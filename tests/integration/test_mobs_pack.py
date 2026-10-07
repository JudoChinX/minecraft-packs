"""Tests pinning the shipped mobs pack.

The pack is its files alone, with no vanilla source to download, and every mob's models and items resolve to files that
exist. Its files under ``assets/minecraft/`` are the items atlas, which only names the client's own illager and pig
textures, and the blockstate of each borrowed block, which only names the client's own block models and the pack's own.
"""

import itertools
import json
import re

import pytest
from PIL import Image

from minecraft_packs.config import load_pack
from tests.helpers import REPO_ROOT

_MOBS = load_pack(REPO_ROOT / 'packs' / 'mobs')
_ASSETS = _MOBS.files_dir / 'assets'
_ITEMS = (
    'jello',
    'harmonizer_tentacle',
    'cooked_harmonizer_tentacle',
    'tropical_slime',
    'orb_of_dominance',
    'ancient_callings',
    'cutlass',
    'peg_leg',
    'crocofang_tooth',
    'throwing_knife',
)
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
    'hopping_pig',
    'pirate_1',
    'pirate_2',
    'pirate_3',
    'pirate_4',
    'pirate_5',
    'pirate_captain',
    'geomancer',
    'infernoillager',
    'simphtomer',
    'crocofang',
)
_BLOCKS = ('moldy_oak_planks', 'fertilized_sand', 'palm_log', 'palm_planks', 'palm_slab')
_BORROWED = {
    'moldy_oak_planks': 'mushroom_stem',
    'palm_log': 'brown_mushroom_block',
    'fertilized_sand': 'red_mushroom_block',
}
# The borrowed slab (mobs 11): the slab's id, its full block's id and the vanilla slab borrowed whole, every state ours.
_SLABS = {'palm_slab': ('palm_planks', 'petrified_oak_slab')}
_FULL_OF = {full: slab for slab, (full, _) in _SLABS.items()}
# A borrowed block drawn as a column: its end texture (mobs 11's palm log, ringed ends).
_COLUMNS = {'palm_log': 'palm_log_top'}
_FACES = ('north', 'east', 'south', 'west', 'up', 'down')
_REFERENCE = re.compile(r'^(bettermodel|mobs):([a-z0-9_/]+)$')
_ATLAS = _ASSETS / 'minecraft' / 'atlases' / 'items.json'
_VANILLA_TEXTURE = re.compile(r'^minecraft:entity/(illager|pig)/[a-z0-9_]+$')


def test_mobs_is_a_resource_pack_for_26_3() -> None:
    """Test the pack is a resource pack declaring format 97, as the enchanter does."""
    assert _MOBS.kind == 'resource'
    assert (_MOBS.min_format, _MOBS.max_format) == (97, 97)


def test_mobs_recolours_nothing() -> None:
    """Test the pack takes nothing from the client jar: no Illusioner recolour, so the build downloads nothing for it.

    The files it may hold under ``assets/minecraft/`` are the items atlas and each borrowed block's blockstate: JSON
    naming vanilla textures and block models, no pixels.
    """
    assert _MOBS.vanilla is None
    assert not _MOBS.textures
    assert _MOBS.preview is None
    shipped = sorted(
        path.relative_to(_ASSETS).as_posix() for path in (_ASSETS / 'minecraft').rglob('*') if path.is_file()
    )
    allowed = ['minecraft/atlases/items.json'] + [f'minecraft/blockstates/{base}.json' for base in _BORROWED.values()]
    allowed += [f'minecraft/blockstates/{base}.json' for _, base in _SLABS.values()]
    assert shipped == sorted(allowed)


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


@pytest.mark.parametrize('block', _BLOCKS)
def test_block_item_resolves(block: str) -> None:
    """Test each borrowed block's item names its block model, which draws the block's own texture, which exists.

    Most are a ``cube_all``; the palm log is a ``cube_column`` with ringed ends, and the palm slab vanilla's ``slab``
    on the palm planks' texture.
    """
    definition = json.loads((_ASSETS / 'mobs' / 'items' / f'{block}.json').read_text())
    assert definition['model']['model'] == f'mobs:block/{block}'
    model = json.loads((_ASSETS / 'mobs' / 'models' / 'block' / f'{block}.json').read_text())
    texture = block
    if block in _COLUMNS:
        assert model['parent'] == 'minecraft:block/cube_column'
        assert model['textures'] == {'end': f'mobs:block/{_COLUMNS[block]}', 'side': f'mobs:block/{block}'}
    elif block in _SLABS:
        texture = _SLABS[block][0]
        assert model['parent'] == 'minecraft:block/slab'
        assert model['textures'] == dict.fromkeys(('bottom', 'side', 'top'), f'mobs:block/{texture}')
    else:
        assert model['parent'] == 'minecraft:block/cube_all'
        assert model['textures'] == {'all': f'mobs:block/{block}'}
    assert (_ASSETS / 'mobs' / 'textures' / 'block' / f'{texture}.png').read_bytes().startswith(b'\x89PNG')


def _matches(when: dict, state: dict) -> bool:
    """Whether a multipart ``when`` holds for a state: every key equal, or any branch of an ``OR``."""
    if 'OR' in when:
        return any(_matches(branch, state) for branch in when['OR'])
    return all(state[key] == value for key, value in when.items())


@pytest.mark.parametrize('block', sorted(_BORROWED))
def test_borrowed_blockstate_draws_the_block_only_in_its_state(block: str) -> None:
    """Test a huge-mushroom block's blockstate draws the block when all six faces are off, and vanilla's in the 63 others.

    Its parts name only vanilla's own models for that block and the pack's own block, and the block's part is the last.
    """
    base = _BORROWED[block]
    blockstate = json.loads((_ASSETS / 'minecraft' / 'blockstates' / f'{base}.json').read_text())
    parts = blockstate['multipart']
    ours = f'mobs:block/{block}'
    vanilla = {f'minecraft:block/{base}', 'minecraft:block/mushroom_block_inside'}
    assert {part['apply']['model'] for part in parts} == vanilla | {ours}
    assert parts[-1]['apply']['model'] == ours
    for values in itertools.product(('true', 'false'), repeat=len(_FACES)):
        state = dict(zip(_FACES, values))
        drawn = [part['apply']['model'] for part in parts if _matches(part.get('when', {}), state)]
        if all(value == 'false' for value in values):
            assert drawn == [ours]
        else:
            assert drawn
            assert ours not in drawn
            assert set(drawn) <= vanilla


@pytest.mark.parametrize('slab', sorted(_SLABS))
def test_borrowed_slab_draws_every_state_as_ours(slab: str) -> None:
    """Test the borrowed slab's blockstate draws its three states on the pack's own models.

    They are the slab, its top half, and the full block for the double.
    """
    full, base = _SLABS[slab]
    blockstate = json.loads((_ASSETS / 'minecraft' / 'blockstates' / f'{base}.json').read_text())
    assert blockstate == {
        'variants': {
            'type=bottom': {'model': f'mobs:block/{slab}'},
            'type=double': {'model': f'mobs:block/{full}'},
            'type=top': {'model': f'mobs:block/{slab}_top'},
        }
    }
    top = json.loads((_ASSETS / 'mobs' / 'models' / 'block' / f'{slab}_top.json').read_text())
    assert top['parent'] == 'minecraft:block/slab_top'


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
