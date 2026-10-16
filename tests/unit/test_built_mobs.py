"""Tests for built_mobs.py: the deterministic built-mobs bundle and its SHA-256 file."""

import hashlib
import zipfile
from pathlib import Path

from minecraft_packs.built_mobs import sha256_path
from minecraft_packs.built_mobs import zip_bundle


def _bundle(root: Path) -> Path:
    """Write a built-mobs directory with two mobs, a model, a README and stray files."""
    src = root / 'built-mobs'
    src.mkdir()
    (src / 'built_zed.json').write_text('{"id": "built_zed"}', encoding='utf-8')
    (src / 'built_ant.json').write_text('{"id": "built_ant"}', encoding='utf-8')
    (src / 'built_ant.bbmodel').write_text('{}', encoding='utf-8')
    (src / 'README.md').write_text('readme', encoding='utf-8')
    (src / 'notes.txt').write_text('stray', encoding='utf-8')
    (src / 'built_Bad.json').write_text('{}', encoding='utf-8')
    (src / 'sub').mkdir()
    return src


def _names(zip_path: Path) -> list[str]:
    """List a zip's entry names."""
    with zipfile.ZipFile(zip_path) as archive:
        return archive.namelist()


def test_zip_is_byte_identical_across_builds(tmp_path: Path) -> None:
    """Test two builds give the same bytes and digest, with sorted, stored, epoch-stamped entries."""
    src = _bundle(tmp_path)

    first = zip_bundle(src, tmp_path / 'one' / 'built-mobs.zip')
    second = zip_bundle(src, tmp_path / 'two' / 'built-mobs.zip')

    assert first == second
    assert (tmp_path / 'one' / 'built-mobs.zip').read_bytes() == (tmp_path / 'two' / 'built-mobs.zip').read_bytes()
    with zipfile.ZipFile(tmp_path / 'one' / 'built-mobs.zip') as archive:
        assert archive.namelist() == ['built_ant.bbmodel', 'built_ant.json', 'built_zed.json']
        assert {info.compress_type for info in archive.infolist()} == {zipfile.ZIP_STORED}
        assert {info.date_time for info in archive.infolist()} == {(1980, 1, 1, 0, 0, 0)}


def test_empty_bundle_is_valid(tmp_path: Path) -> None:
    """Test a directory holding only a README gives a real empty zip."""
    src = tmp_path / 'built-mobs'
    src.mkdir()
    (src / 'README.md').write_text('readme', encoding='utf-8')

    digest = zip_bundle(src, tmp_path / 'built-mobs.zip')

    data = (tmp_path / 'built-mobs.zip').read_bytes()
    assert data[:4] == b'PK\x05\x06'
    assert _names(tmp_path / 'built-mobs.zip') == []
    assert digest == hashlib.sha256(data).hexdigest()


def test_readme_excluded(tmp_path: Path) -> None:
    """Test the README, stray files, badly named files and directories stay out of the zip."""
    zip_bundle(_bundle(tmp_path), tmp_path / 'built-mobs.zip')

    names = _names(tmp_path / 'built-mobs.zip')
    assert 'README.md' not in names
    assert names == ['built_ant.bbmodel', 'built_ant.json', 'built_zed.json']


def test_sha_file_format(tmp_path: Path) -> None:
    """Test the SHA-256 file is one sha256sum-format line naming the zip."""
    digest = zip_bundle(_bundle(tmp_path), tmp_path / 'dist' / 'built-mobs.zip')

    sha_file = tmp_path / 'dist' / 'built-mobs.sha256'
    assert sha256_path(tmp_path / 'dist' / 'built-mobs.zip') == sha_file
    assert sha_file.read_text(encoding='utf-8') == f'{digest}  built-mobs.zip\n'
    assert digest == hashlib.sha256((tmp_path / 'dist' / 'built-mobs.zip').read_bytes()).hexdigest()
