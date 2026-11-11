"""Tests for built_structures.py: the deterministic built-structures bundle and its SHA-256 file."""

import hashlib
import zipfile
from pathlib import Path

import pytest

from minecraft_packs.built_mobs import sha256_path
from minecraft_packs.built_structures import MAX_STRUCTURES
from minecraft_packs.built_structures import zip_bundle
from minecraft_packs.errors import PackError

EMPTY_ZIP_SIZE = 22


def _bundle(root: Path) -> Path:
    """Write a built-structures directory with two structures, a README and stray files."""
    src = root / 'built-structures'
    src.mkdir()
    (src / 'built_zed.nbt').write_bytes(b'\x1f\x8bzed')
    (src / 'built_zed.json').write_text('{"name": "zed"}', encoding='utf-8')
    (src / 'built_ant_hill.nbt').write_bytes(b'\x1f\x8bant')
    (src / 'built_ant_hill.json').write_text('{"name": "ant_hill"}', encoding='utf-8')
    (src / 'README.md').write_text('readme', encoding='utf-8')
    (src / 'notes.txt').write_text('stray', encoding='utf-8')
    (src / 'built_Bad.nbt').write_bytes(b'x')
    (src / 'built_ant.bbmodel').write_text('{}', encoding='utf-8')
    (src / 'built_dir.nbt').mkdir()
    (src / 'built_a__b.nbt').write_bytes(b'x')
    return src


def _names(zip_path: Path) -> list[str]:
    """List a zip's entry names."""
    with zipfile.ZipFile(zip_path) as archive:
        return archive.namelist()


def test_zip_is_byte_identical_across_builds(tmp_path: Path) -> None:
    """Test two builds give the same bytes and digest, with sorted, stored, epoch-stamped entries."""
    src = _bundle(tmp_path)

    first = zip_bundle(src, tmp_path / 'one' / 'built-structures.zip')
    second = zip_bundle(src, tmp_path / 'two' / 'built-structures.zip')

    assert first == second
    one = (tmp_path / 'one' / 'built-structures.zip').read_bytes()
    assert one == (tmp_path / 'two' / 'built-structures.zip').read_bytes()
    with zipfile.ZipFile(tmp_path / 'one' / 'built-structures.zip') as archive:
        assert archive.namelist() == ['built_ant_hill.json', 'built_ant_hill.nbt', 'built_zed.json', 'built_zed.nbt']
        assert archive.read('built_zed.nbt') == b'\x1f\x8bzed'
        assert {info.compress_type for info in archive.infolist()} == {zipfile.ZIP_STORED}
        assert {info.date_time for info in archive.infolist()} == {(1980, 1, 1, 0, 0, 0)}


def test_empty_bundle_is_the_22_byte_zip(tmp_path: Path) -> None:
    """Test a directory holding only a README gives the real, 22-byte empty zip."""
    src = tmp_path / 'built-structures'
    src.mkdir()
    (src / 'README.md').write_text('readme', encoding='utf-8')

    digest = zip_bundle(src, tmp_path / 'built-structures.zip')

    data = (tmp_path / 'built-structures.zip').read_bytes()
    assert len(data) == EMPTY_ZIP_SIZE
    assert data[:4] == b'PK\x05\x06'
    assert digest == hashlib.sha256(data).hexdigest()


def test_readme_and_other_names_excluded(tmp_path: Path) -> None:
    """Test the README, stray files, badly named files, models and directories stay out of the zip."""
    zip_bundle(_bundle(tmp_path), tmp_path / 'built-structures.zip')

    names = _names(tmp_path / 'built-structures.zip')
    assert 'README.md' not in names
    assert names == ['built_ant_hill.json', 'built_ant_hill.nbt', 'built_zed.json', 'built_zed.nbt']


def test_sha_file_format(tmp_path: Path) -> None:
    """Test the SHA-256 file is one sha256sum-format line naming the zip."""
    zip_path = tmp_path / 'dist' / 'built-structures.zip'

    digest = zip_bundle(_bundle(tmp_path), zip_path)

    assert sha256_path(zip_path).read_text(encoding='utf-8') == f'{digest}  built-structures.zip\n'
    assert digest == hashlib.sha256(zip_path.read_bytes()).hexdigest()


def test_unpaired_file_is_an_error(tmp_path: Path) -> None:
    """Test a .nbt without its .json, or the reverse, fails before a release."""
    src = tmp_path / 'built-structures'
    src.mkdir()
    (src / 'built_ant.nbt').write_bytes(b'x')
    (src / 'built_bee.json').write_text('{}', encoding='utf-8')

    with pytest.raises(PackError, match='built_ant, built_bee'):
        zip_bundle(src, tmp_path / 'built-structures.zip')


def test_too_many_structures_is_an_error(tmp_path: Path) -> None:
    """Test 50 structures pass and 51 fail."""
    src = tmp_path / 'built-structures'
    src.mkdir()
    for number in range(MAX_STRUCTURES):
        (src / f'built_s{number}.nbt').write_bytes(b'x')
        (src / f'built_s{number}.json').write_text('{}', encoding='utf-8')
    zip_bundle(src, tmp_path / 'built-structures.zip')
    (src / 'built_extra.nbt').write_bytes(b'x')
    (src / 'built_extra.json').write_text('{}', encoding='utf-8')

    with pytest.raises(PackError, match='51 structures'):
        zip_bundle(src, tmp_path / 'built-structures.zip')
