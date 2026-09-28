"""Tests for build.py: assembling pack entries, building zips and rendering previews."""

import json
from pathlib import Path

import pytest
from PIL import Image

from minecraft_packs import build
from minecraft_packs.build import build_pack
from minecraft_packs.build import pack_entries
from minecraft_packs.build import preview_pack
from minecraft_packs.build import record_expected_sha1
from minecraft_packs.build import vanilla_textures
from minecraft_packs.config import load_pack
from minecraft_packs.errors import PackError
from tests.builders import ClientJarBuilder
from tests.builders import PackBuilder
from tests.helpers import FIXTURE_ASSET
from tests.helpers import fixture_bytes

_JAR = ClientJarBuilder().build()


def test_build_pack_writes_zip_and_sidecar(tmp_path: Path) -> None:
    """Test a build writes <name>-<version>.zip and its sidecar, and reports what it did."""
    pack = load_pack(PackBuilder().recolouring(_JAR).build(tmp_path / 'packs'))
    jar_path = ClientJarBuilder().write(tmp_path / 'client.jar')

    result = build_pack(pack, '1.2.3', tmp_path / 'dist', tmp_path / 'cache', jar_path)

    assert result.zip_path == tmp_path / 'dist' / 'test-1.2.3.zip'
    assert result.size == result.zip_path.stat().st_size
    assert (tmp_path / 'dist' / 'test-1.2.3.zip.sha1').read_text(encoding='utf-8').split()[0] == result.sha1
    assert result.counts == {FIXTURE_ASSET: {'robe': 1, 'trim': 1}}


def test_build_pack_fails_when_verification_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a zip that fails its own verification fails the build."""
    pack = load_pack(PackBuilder().with_file('pack.png', fixture_bytes()).build(tmp_path / 'packs'))
    monkeypatch.setattr(build, 'verify_zip', lambda zip_path: ['broken'])

    with pytest.raises(PackError, match='failed verification: broken'):
        build_pack(pack, '1.2.3', tmp_path / 'dist', tmp_path / 'cache')

    assert not list((tmp_path / 'dist').iterdir())


def test_pack_entries_recolouring(tmp_path: Path) -> None:
    """Test a recolouring pack yields pack.mcmeta, the recoloured texture and a generated icon."""
    pack = load_pack(PackBuilder().recolouring(_JAR).build(tmp_path))
    vanilla = vanilla_textures(pack, tmp_path, ClientJarBuilder().write(tmp_path / 'client.jar'))

    entries, counts = pack_entries(pack, vanilla)

    assert sorted(entries) == [FIXTURE_ASSET, 'pack.mcmeta', 'pack.png']
    assert json.loads(entries['pack.mcmeta']) == pack.mcmeta()
    assert entries['pack.mcmeta'].endswith(b'}\n')
    assert counts == {FIXTURE_ASSET: {'robe': 1, 'trim': 1}}


def test_pack_entries_rejects_clash(tmp_path: Path) -> None:
    """Test a static file may not overwrite a generated one."""
    pack = load_pack(PackBuilder().recolouring(_JAR).with_file('pack.png', b'icon').build(tmp_path))
    vanilla = vanilla_textures(pack, tmp_path, ClientJarBuilder().write(tmp_path / 'client.jar'))

    with pytest.raises(PackError, match='would overwrite generated file\\(s\\): pack.png'):
        pack_entries(pack, vanilla)


def test_pack_entries_requires_icon(tmp_path: Path) -> None:
    """Test a pack with neither a preview nor files/pack.png is refused."""
    pack = load_pack(PackBuilder().build(tmp_path))

    with pytest.raises(PackError, match='no pack.png'):
        pack_entries(pack, {})


def test_pack_entries_static_files(tmp_path: Path) -> None:
    """Test files/ is copied verbatim, dotfiles excepted, with no vanilla assets needed."""
    builder = PackBuilder().with_file('pack.png', fixture_bytes()).with_file('assets/test/models/mob.json', b'{}')
    pack = load_pack(builder.with_file('.DS_Store', b'x').with_file('assets/.hidden/x.json', b'x').build(tmp_path))

    entries, counts = pack_entries(pack, vanilla_textures(pack, tmp_path))

    assert sorted(entries) == ['assets/test/models/mob.json', 'pack.mcmeta', 'pack.png']
    assert entries['assets/test/models/mob.json'] == b'{}'
    assert not counts


def test_preview_pack(tmp_path: Path) -> None:
    """Test the review sheet is written as a PNG, creating its directory."""
    pack = load_pack(PackBuilder().recolouring(_JAR).build(tmp_path / 'packs'))
    jar_path = ClientJarBuilder().write(tmp_path / 'client.jar')

    out_path = preview_pack(pack, tmp_path / 'out' / 'preview.png', tmp_path / 'cache', jar_path)

    with Image.open(out_path) as sheet:
        assert (sheet.format, sheet.mode) == ('PNG', 'RGB')


def test_preview_pack_requires_preview(tmp_path: Path) -> None:
    """Test a pack without [preview] cannot be previewed."""
    pack = load_pack(PackBuilder().build(tmp_path))

    with pytest.raises(PackError, match='nothing to preview'):
        preview_pack(pack, tmp_path / 'preview.png', tmp_path / 'cache')


def test_record_expected_sha1(tmp_path: Path) -> None:
    """Test the SHA-1 is written to the pack's expected.sha1, and read back on the next load."""
    pack = load_pack(PackBuilder().build(tmp_path))

    path = record_expected_sha1(pack, 'b' * 40)

    assert path.read_text(encoding='utf-8') == f'{"b" * 40}\n'
    assert load_pack(pack.directory).expected_sha1 == 'b' * 40


def test_vanilla_textures_verifies_local_jar(tmp_path: Path) -> None:
    """Test a local jar that differs from the pin is refused before any asset is read."""
    pack = load_pack(PackBuilder().recolouring(_JAR).build(tmp_path))
    jar_path = ClientJarBuilder().with_asset('assets/extra.png', b'x').write(tmp_path / 'client.jar')

    with pytest.raises(PackError, match='does not match the pinned'):
        vanilla_textures(pack, tmp_path, jar_path)
