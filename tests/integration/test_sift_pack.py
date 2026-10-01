"""Tests pinning the shipped sift data pack: its kind, format, and that its references resolve."""

import json
import re
from pathlib import Path

import pytest

from minecraft_packs.build import pack_entries
from minecraft_packs.config import load_pack
from tests.helpers import REPO_ROOT

_SIFT = load_pack(REPO_ROOT / 'packs' / 'sift')
_DATA = _SIFT.files_dir / 'data' / 'sift'
_REFERENCE = re.compile(r'^sift:([a-z0-9_/]+)$')


def _strings(value: object) -> list[str]:
    """Every string anywhere in a JSON value."""
    if isinstance(value, dict):
        value = list(value.values())
    if isinstance(value, list):
        return [found for item in value for found in _strings(item)]
    return [value] if isinstance(value, str) else []


def _json_files() -> list[Path]:
    return sorted(_DATA.rglob('*.json'))


def test_sift_is_a_data_pack_for_26_3() -> None:
    """Test the pack is a data pack declaring format 121, the 26.3 data pack format."""
    assert _SIFT.kind == 'data'
    assert (_SIFT.min_format, _SIFT.max_format) == (121, 121)


def test_sift_entries_build() -> None:
    """Test the pack assembles: only data/ files, pack.png and pack.mcmeta."""
    entries, _ = pack_entries(_SIFT, {})

    assert all(name.startswith('data/sift/') or name in {'pack.mcmeta', 'pack.png'} for name in entries)
    assert 'data/sift/dimension/the_sift.json' in entries


@pytest.mark.parametrize('path', _json_files(), ids=lambda p: p.relative_to(_DATA).as_posix())
def test_sift_references_resolve(path: Path) -> None:
    """Test every sift:<id> a file names is a file in the pack."""
    defined = {p.relative_to(_DATA).with_suffix('').as_posix() for p in _json_files()}
    for value in _strings(json.loads(path.read_text(encoding='utf-8'))):
        match = _REFERENCE.match(value)
        if match:
            assert any(d.endswith('/' + match.group(1)) for d in defined), f'{value} does not resolve'


def test_sift_dimension_uses_its_own_surface() -> None:
    """Test the dimension's noise settings route to the pack's material rule, and both biomes are placed."""
    dimension = json.loads((_DATA / 'dimension' / 'the_sift.json').read_text(encoding='utf-8'))
    settings = json.loads((_DATA / 'worldgen' / 'noise_settings' / 'sift.json').read_text(encoding='utf-8'))

    assert dimension['generator']['settings'] == 'sift:sift'
    assert settings['material_rule'] == 'sift:sift'
    biomes = {entry['biome'] for entry in dimension['generator']['biome_source']['biomes']}
    assert biomes == {'sift:singers_meadow', 'sift:carapace'}
