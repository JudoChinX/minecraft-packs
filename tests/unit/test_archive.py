"""Tests for archive.py: deterministic zips, SHA-1 sidecars and offline verification."""

import zipfile
from pathlib import Path

import pytest

from minecraft_packs.archive import ZIP_EPOCH
from minecraft_packs.archive import sha1_hex
from minecraft_packs.archive import sidecar_path
from minecraft_packs.archive import verify_zip
from minecraft_packs.archive import write_zip
from tests.builders import ZipBuilder
from tests.helpers import fixture_bytes
from tests.helpers import sha1_of

_ENTRIES = {
    'pack.mcmeta': b'{"pack": {"description": "Test pack", "pack_format": 97}}',
    'pack.png': fixture_bytes(),
    'assets/minecraft/textures/entity/test/mob.png': fixture_bytes(),
}

_verify_zip_cases = {
    'bad_png': {
        'builder': ZipBuilder().with_entry('assets/minecraft/textures/test.png', b'not a png'),
        'expected': ['assets/minecraft/textures/test.png: not a readable PNG'],
    },
    'deflated_entry': {
        'builder': ZipBuilder().with_entry('pack.png', fixture_bytes(), compress_type=zipfile.ZIP_DEFLATED),
        'expected': ['pack.png: compressed; entries must be stored'],
    },
    'directory_entry': {
        'builder': ZipBuilder().with_entry('pack.png/', b''),
        'expected': ['pack.png/: directory entry'],
    },
    'format_list': {
        'builder': ZipBuilder().with_mcmeta({'pack': {'description': 'x', 'min_format': [97, 1], 'max_format': 97}}),
        'expected': [],
    },
    'format_list_too_long': {
        'builder': ZipBuilder().with_mcmeta({'pack': {'description': 'x', 'pack_format': [97, 1, 2]}}),
        'expected': ['pack.mcmeta declares neither pack_format nor min_format and max_format'],
    },
    'format_boolean': {
        'builder': ZipBuilder().with_mcmeta({'pack': {'description': 'x', 'pack_format': True}}),
        'expected': ['pack.mcmeta declares neither pack_format nor min_format and max_format'],
    },
    'icon_missing': {
        'builder': ZipBuilder().without('pack.png'),
        'expected': ['pack.png is missing'],
    },
    'icon_not_square': {
        'builder': ZipBuilder().with_png('pack.png', (64, 32)),
        'expected': ['pack.png is 64x32, not square'],
    },
    'mcmeta_missing': {
        'builder': ZipBuilder().without('pack.mcmeta'),
        'expected': ['pack.mcmeta is missing'],
    },
    'mcmeta_not_json': {
        'builder': ZipBuilder().with_entry('pack.mcmeta', b'\xff{'),
        'expected': ['pack.mcmeta is not valid UTF-8 JSON'],
    },
    'mode': {
        'builder': ZipBuilder().with_entry('pack.png', fixture_bytes(), mode=0o100755),
        'expected': ['pack.png: mode 100755 is not 100644'],
    },
    'no_description': {
        'builder': ZipBuilder().with_mcmeta({'pack': {'pack_format': 97}}),
        'expected': ['pack.mcmeta has no pack description'],
    },
    'no_formats': {
        'builder': ZipBuilder().with_mcmeta({'pack': {'description': 'x', 'min_format': 97}}),
        'expected': ['pack.mcmeta declares neither pack_format nor min_format and max_format'],
    },
    'no_pack_object': {
        'builder': ZipBuilder().with_mcmeta(['pack']),
        'expected': ['pack.mcmeta has no "pack" object'],
    },
    'pack_format_only': {
        'builder': ZipBuilder().with_mcmeta({'pack': {'description': 'x', 'pack_format': 34}}),
        'expected': [],
    },
    'sound': {
        'builder': ZipBuilder(),
        'expected': [],
    },
    'timestamp': {
        'builder': ZipBuilder().with_entry('pack.png', fixture_bytes(), date_time=(2026, 9, 28, 12, 0, 0)),
        'expected': ['pack.png: timestamp (2026, 9, 28, 12, 0, 0) is not the zip epoch'],
    },
    'unsorted': {
        'builder': ZipBuilder().unsorted(),
        'expected': ['entries are not sorted'],
    },
}


def test_sha1_hex() -> None:
    """Test sha1_hex returns the lowercase hexadecimal SHA-1."""
    assert sha1_hex(b'abc') == 'a9993e364706816aba3e25717850c26c9cd0d89d'


def test_sidecar_path() -> None:
    """Test the sidecar sits beside the zip with .sha1 appended."""
    assert sidecar_path(Path('dist/test-1.0.zip')) == Path('dist/test-1.0.zip.sha1')


@pytest.mark.parametrize(
    'builder, expected',
    [(case['builder'], case['expected']) for case in _verify_zip_cases.values()],
    ids=list(_verify_zip_cases.keys()),
)
def test_verify_zip(tmp_path: Path, builder: ZipBuilder, expected: list[str]) -> None:
    """Test verify_zip reports each way a pack zip can be malformed, and nothing for a sound one."""
    assert verify_zip(builder.build(tmp_path / 'test.zip')) == expected


def test_verify_zip_missing_file(tmp_path: Path) -> None:
    """Test a zip that does not exist is reported, not raised."""
    missing = tmp_path / 'missing.zip'

    assert verify_zip(missing) == [f'{missing}: no such file']


def test_verify_zip_not_a_zip(tmp_path: Path) -> None:
    """Test a file that is not a zip is reported, not raised."""
    path = tmp_path / 'test.zip'
    path.write_bytes(b'not a zip')

    assert verify_zip(path) == ['not a zip file, or a corrupt one']


def test_verify_zip_sidecar_mismatch(tmp_path: Path) -> None:
    """Test a sidecar that no longer matches the zip is reported."""
    zip_path = tmp_path / 'test.zip'
    digest = write_zip(_ENTRIES, zip_path)
    sidecar_path(zip_path).write_text('0' * 40 + '  test.zip\n', encoding='utf-8')

    assert verify_zip(zip_path) == [f'test.zip.sha1 does not match the zip (zip SHA-1 is {digest})']


def test_verify_zip_sidecar_empty(tmp_path: Path) -> None:
    """Test an empty sidecar is reported as a mismatch."""
    zip_path = tmp_path / 'test.zip'
    digest = write_zip(_ENTRIES, zip_path)
    sidecar_path(zip_path).write_text('', encoding='utf-8')

    assert verify_zip(zip_path) == [f'test.zip.sha1 does not match the zip (zip SHA-1 is {digest})']


def test_write_zip_is_deterministic(tmp_path: Path) -> None:
    """Test the same entries in any order produce byte-identical zips."""
    first = tmp_path / 'first' / 'test.zip'
    second = tmp_path / 'second' / 'test.zip'

    first_sha1 = write_zip(_ENTRIES, first)
    second_sha1 = write_zip(dict(reversed(_ENTRIES.items())), second)

    assert first.read_bytes() == second.read_bytes()
    assert first_sha1 == second_sha1 == sha1_of(first.read_bytes())


def test_write_zip_layout(tmp_path: Path) -> None:
    """Test entries are sorted, stored, stamped with the zip epoch and mode 0644, with no directories."""
    zip_path = tmp_path / 'test.zip'

    write_zip(_ENTRIES, zip_path)

    with zipfile.ZipFile(zip_path) as archive:
        infos = archive.infolist()
        assert [info.filename for info in infos] == sorted(_ENTRIES)
        assert all(info.date_time == ZIP_EPOCH for info in infos)
        assert all(info.external_attr >> 16 == 0o100644 for info in infos)
        assert all(info.compress_type == zipfile.ZIP_STORED for info in infos)
        assert {info.filename: archive.read(info) for info in infos} == _ENTRIES


def test_write_zip_writes_sidecar(tmp_path: Path) -> None:
    """Test the sidecar is in sha1sum format and passes verification."""
    zip_path = tmp_path / 'test.zip'

    digest = write_zip(_ENTRIES, zip_path)

    assert sidecar_path(zip_path).read_text(encoding='utf-8') == f'{digest}  test.zip\n'
    assert verify_zip(zip_path) == []
