"""Tests pinning the shipped mobs pack.

The Enchanter's rules stay in step with the enchanter pack, and the Sift mobs' models and items resolve to files that
exist.
"""

import json
import re

import pytest

from minecraft_packs.config import load_pack
from tests.helpers import REPO_ROOT

_MOBS = load_pack(REPO_ROOT / 'packs' / 'mobs')
_ENCHANTER = load_pack(REPO_ROOT / 'packs' / 'enchanter')
_ASSETS = _MOBS.files_dir / 'assets'
_ITEMS = ('jello', 'harmonizer_tentacle', 'cooked_harmonizer_tentacle', 'tropical_slime')
_MODELS = (
    'blob',
    'sifter',
    'harmonizer',
    'twisted_harmonizer',
    'soul_zombie',
    'soul_husk',
    'soul_drowned',
    'soul_skeleton',
    'soul_stray',
    'soul_creeper',
    'soul_spider',
    'soul_zombie_villager',
    'sculk_sniffer',
    'jellyfish',
    'tropical_fish_slime',
    'tuff_golem',
)
_REFERENCE = re.compile(r'^(bettermodel|mobs):([a-z0-9_/]+)$')


def test_mobs_is_a_resource_pack_for_26_3() -> None:
    """Test the pack is a resource pack declaring format 97, as the enchanter does."""
    assert _MOBS.kind == 'resource'
    assert (_MOBS.min_format, _MOBS.max_format) == (97, 97)


def test_enchanter_rules_are_the_enchanter_packs() -> None:
    """Test the mobs pack recolours the Illusioner exactly as the enchanter pack does."""
    assert _MOBS.vanilla == _ENCHANTER.vanilla
    assert _MOBS.textures == _ENCHANTER.textures
    assert _MOBS.preview == _ENCHANTER.preview


@pytest.mark.parametrize('item', _ITEMS)
def test_item_definition_resolves(item: str) -> None:
    """Test each item definition names a model drawn with the item's own texture, which exists.

    Most items are flat (`layer0`); the Tropical Slime is a cube whose faces use `texture`.
    """
    definition = json.loads((_ASSETS / 'mobs' / 'items' / f'{item}.json').read_text())
    assert definition['model']['model'] == f'mobs:item/{item}'
    model = json.loads((_ASSETS / 'mobs' / 'models' / 'item' / f'{item}.json').read_text())
    assert f'mobs:item/{item}' in model['textures'].values()
    assert (_ASSETS / 'mobs' / 'textures' / 'item' / f'{item}.png').read_bytes().startswith(b'\x89PNG')


@pytest.mark.parametrize('model', _MODELS)
def test_every_mob_has_display_models(model: str) -> None:
    """Test BetterModel's output carries item definitions for every mob."""
    assert list((_ASSETS / 'bettermodel' / 'items' / 'model').glob(f'{model}_*.json'))


def test_every_reference_resolves() -> None:
    """Test every namespaced model and texture reference in the pack's own files points at a file in the pack."""
    missing = []
    for path in sorted(_ASSETS.rglob('*.json')):
        for ref in _strings(json.loads(path.read_text())):
            match = _REFERENCE.match(ref)
            if not match:
                continue
            namespace, rest = match.groups()
            candidates = [
                _ASSETS / namespace / 'models' / f'{rest}.json',
                _ASSETS / namespace / 'textures' / f'{rest}.png',
            ]
            if not any(c.is_file() for c in candidates):
                missing.append(f'{path.relative_to(_ASSETS)}: {ref}')
    assert not missing


def _strings(value: object) -> list[str]:
    """Every string anywhere in a JSON value."""
    if isinstance(value, dict):
        value = list(value.values())
    if isinstance(value, list):
        return [found for item in value for found in _strings(item)]
    return [value] if isinstance(value, str) else []
