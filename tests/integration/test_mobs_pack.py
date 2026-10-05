"""Tests pinning the shipped mobs pack.

The pack is its files alone, with no vanilla source to download, and every mob's models and items resolve to files that
exist. Its one file under ``assets/minecraft/`` is the items atlas, which only names the client's own illager and pig
textures.
"""

import json
import re

import pytest
from PIL import Image

from minecraft_packs.config import load_pack
from tests.helpers import REPO_ROOT

_MOBS = load_pack(REPO_ROOT / 'packs' / 'mobs')
_ASSETS = _MOBS.files_dir / 'assets'
_ITEMS = ('jello', 'harmonizer_tentacle', 'cooked_harmonizer_tentacle', 'tropical_slime', 'orb_of_dominance')
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
    'bear',
    'piston_golem',
    'enchanter',
    'summoner',
    'arch_illager',
)
_REFERENCE = re.compile(r'^(bettermodel|mobs):([a-z0-9_/]+)$')
_ATLAS = _ASSETS / 'minecraft' / 'atlases' / 'items.json'
_VANILLA_TEXTURE = re.compile(r'^minecraft:entity/(illager|pig)/[a-z0-9_]+$')


def test_mobs_is_a_resource_pack_for_26_3() -> None:
    """Test the pack is a resource pack declaring format 97, as the enchanter does."""
    assert _MOBS.kind == 'resource'
    assert (_MOBS.min_format, _MOBS.max_format) == (97, 97)


def test_mobs_recolours_nothing() -> None:
    """Test the pack takes nothing from the client jar: no Illusioner recolour, so the build downloads nothing for it.

    The one file it may hold under ``assets/minecraft/`` is the items atlas: a JSON naming vanilla textures, no pixels.
    """
    assert _MOBS.vanilla is None
    assert not _MOBS.textures
    assert _MOBS.preview is None
    shipped = sorted(
        path.relative_to(_ASSETS).as_posix() for path in (_ASSETS / 'minecraft').rglob('*') if path.is_file()
    )
    assert shipped == ['minecraft/atlases/items.json']


def test_atlas_only_maps_illager_and_pig_textures_onto_the_packs_own_sprites() -> None:
    """Test the items atlas only puts the client's own illager and pig textures under the pack's own sprite names.

    Each source is a ``minecraft:single`` from ``minecraft:entity/illager/*`` or ``minecraft:entity/pig/*`` onto a
    ``bettermodel:`` or ``mobs:`` sprite whose original stand-in PNG the pack ships, so a client that ignores the atlas
    still has a texture to show.
    """
    atlas = json.loads(_ATLAS.read_text())
    assert list(atlas) == ['sources']
    assert atlas['sources']
    sprites = []
    for source in atlas['sources']:
        assert set(source) == {'type', 'resource', 'sprite'}
        assert source['type'] == 'minecraft:single'
        assert _VANILLA_TEXTURE.fullmatch(source['resource'])
        match = _REFERENCE.match(source['sprite'])
        assert match
        namespace, rest = match.groups()
        assert (_ASSETS / namespace / 'textures' / f'{rest}.png').is_file()
        sprites.append(source['sprite'])
    assert len(set(sprites)) == len(sprites)


def test_icon_is_a_square_png() -> None:
    """Test the pack ships its own icon, since without a [preview] none is generated."""
    with Image.open(_MOBS.files_dir / 'pack.png') as icon:
        assert icon.format == 'PNG'
        assert icon.size == (128, 128)


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
