"""Tests pinning the shipped rift data pack: its kind, format, references, and the Rift's worldgen numbers."""

import json
import re
from pathlib import Path
from typing import Any

import pytest

from minecraft_packs.build import pack_entries
from minecraft_packs.config import load_pack
from tests.helpers import REPO_ROOT

_RIFT = load_pack(REPO_ROOT / 'packs' / 'rift')
_DATA = _RIFT.files_dir / 'data' / 'paradox'
_REFERENCE = re.compile(r'^paradox:([a-z0-9_/]+)$')
_ORES = ('eatherite', 'pirelite', 'paralite', 'abyslite')
_ORE_TARGETS = ['minecraft:stone_ore_replaceables', 'minecraft:deepslate_ore_replaceables']


def _strings(value: object) -> list[str]:
    """Every string anywhere in a JSON value."""
    if isinstance(value, dict):
        value = list(value.values())
    if isinstance(value, list):
        return [found for item in value for found in _strings(item)]
    return [value] if isinstance(value, str) else []


def _json_files() -> list[Path]:
    return sorted(_DATA.rglob('*.json'))


def _read(relative: str) -> Any:
    """The JSON file at a path under data/paradox/."""
    return json.loads((_DATA / relative).read_text(encoding='utf-8'))


def _modifier(placed: dict[str, Any], kind: str) -> dict[str, Any]:
    """The one placement modifier of a type in a placed feature."""
    found = [m for m in placed['placement'] if m['type'] == f'minecraft:{kind}']
    assert len(found) == 1, f'{kind}: {found}'
    return found[0]


def _features(biome: str) -> list[str]:
    """Every placed feature a biome lists, over all its steps."""
    return [feature for step in _read(f'worldgen/biome/{biome}.json')['features'] for feature in step]


def _state_string(state: dict[str, Any]) -> str:
    """A block state as BorrowedBlock.blockData() writes it: id[key=value,...], keys sorted."""
    properties = ','.join(f'{key}={value}' for key, value in sorted(state['properties'].items()))
    return f'{state["id"]}[{properties}]'


def test_rift_is_a_data_pack_for_26_3() -> None:
    """Test the pack is a data pack declaring format 121, the 26.3 data pack format."""
    assert _RIFT.kind == 'data'
    assert (_RIFT.min_format, _RIFT.max_format) == (121, 121)


def test_rift_entries_build() -> None:
    """Test the pack assembles: only data/paradox/ files, pack.png and pack.mcmeta, with the dimension."""
    entries, _ = pack_entries(_RIFT, {})

    assert all(name.startswith('data/paradox/') or name in {'pack.mcmeta', 'pack.png'} for name in entries)
    assert 'data/paradox/dimension/rift.json' in entries
    assert 'data/paradox/loot_table/chests/ancient_ruin.json' in entries


@pytest.mark.parametrize('path', _json_files(), ids=lambda p: p.relative_to(_DATA).as_posix())
def test_rift_references_resolve(path: Path) -> None:
    """Test every paradox:<id> a file names is a file in the pack."""
    defined = {p.relative_to(_DATA).with_suffix('').as_posix() for p in _json_files()}
    for value in _strings(json.loads(path.read_text(encoding='utf-8'))):
        match = _REFERENCE.match(value)
        if match:
            assert any(d.endswith('/' + match.group(1)) for d in defined), f'{value} does not resolve'


def test_rift_dimension_type_height() -> None:
    """Test the dimension type reaches y -416 to 320, both multiples of 16, with respawn anchors and raids off."""
    dimension_type = _read('dimension_type/rift.json')

    assert (dimension_type['min_y'], dimension_type['height'], dimension_type['logical_height']) == (-416, 736, 736)
    assert dimension_type['min_y'] % 16 == 0
    assert dimension_type['height'] % 16 == 0
    assert dimension_type['attributes']['minecraft:gameplay/respawn_anchor_works'] is False
    assert dimension_type['attributes']['minecraft:gameplay/can_start_raid'] is False


def test_rift_biomes_have_no_carvers() -> None:
    """Test neither biome lists a carver: a vanilla cave carver would fill the deep stone with lava."""
    for biome in ('the_rift', 'primary_cave'):
        assert not _read(f'worldgen/biome/{biome}.json')['carvers'], biome


def test_rift_noise_settings_widened() -> None:
    """Test the noise settings match the dimension type's height and route to the pack's own material rule."""
    settings = _read('worldgen/noise_settings/rift.json')
    dimension = _read('dimension/rift.json')

    assert (settings['noise']['min_y'], settings['noise']['height']) == (-416, 736)
    assert settings['material_rule'] == 'paradox:rift'
    assert dimension['generator']['settings'] == 'paradox:rift'
    assert dimension['type'] == 'paradox:rift'
    biomes = {entry['biome'] for entry in dimension['generator']['biome_source']['biomes']}
    assert biomes == {'paradox:the_rift', 'paradox:primary_cave'}


def test_rift_ore_features_place_the_four_states() -> None:
    """Test each ore feature places its ORE_STATES line, in stone and deepslate, in that order of ores."""
    lines = (_RIFT.directory / 'ORE_STATES').read_text(encoding='utf-8').splitlines()

    assert len(lines) == len(_ORES)
    for ore, line in zip(_ORES, lines, strict=True):
        feature = _read(f'worldgen/feature/{ore}_ore.json')
        tags = [target['target']['tag'] for target in feature['targets'] if 'tag' in target['target']]
        assert feature['type'] == 'minecraft:ore'
        assert tags == _ORE_TARGETS, ore
        assert {_state_string(target['state']) for target in feature['targets']} == {line}, ore


@pytest.mark.parametrize(
    ('ore', 'bottom', 'top', 'size', 'count', 'discard'),
    [
        ('eatherite', -64, 100, 6, 6, 0.0),
        ('pirelite', -100, 0, 4, 3, 0.0),
        ('paralite', -200, -40, 3, 2, 0.0),
        # One vein in 5 chunks (a rarity filter, not a count): the 2026-10-26 settlement, size 3 and discard 0.5,
        # since a size-2 vein with discard 1.0 places nothing on 26.3.
        ('abyslite', -400, -120, 3, None, 0.5),
    ],
)
def test_rift_ore_ranges(ore: str, bottom: int, top: int, size: int, count: int | None, discard: float) -> None:
    """Test each ore's height range, vein size, veins per chunk and air-exposure discard."""
    feature = _read(f'worldgen/feature/{ore}_ore.json')
    placed = _read(f'worldgen/placed_feature/{ore}_ore.json')
    height = _modifier(placed, 'height_range')['height']

    assert placed['feature'] == f'paradox:{ore}_ore'
    assert (feature['size'], feature['discard_chance_on_air_exposure']) == (size, discard)
    if count is None:
        assert _modifier(placed, 'rarity_filter')['chance'] == 5
        assert not [m for m in placed['placement'] if m['type'] == 'minecraft:count']
    else:
        assert _modifier(placed, 'count')['count'] == count
    assert height['type'] == 'minecraft:uniform'
    assert (height['min_inclusive'], height['max_inclusive']) == ({'absolute': bottom}, {'absolute': top})
    assert placed['placement'][-1] == {'type': 'minecraft:biome'}


def test_rift_pirelite_ore_lava_is_kept_beside_lava_or_magma() -> None:
    """Test the second pirelite placement: the same feature, 6 a chunk, kept only near lava or magma."""
    placed = _read('worldgen/placed_feature/pirelite_ore_lava.json')
    near = json.dumps(_modifier(placed, 'block_predicate_filter')['predicate'])

    assert placed['feature'] == 'paradox:pirelite_ore'
    assert _modifier(placed, 'count')['count'] == 6
    assert 'minecraft:lava' in near
    assert 'minecraft:magma_block' in near
    assert 'paradox:pirelite_ore_lava' in _features('the_rift')
    assert 'paradox:pirelite_ore_lava' in _features('primary_cave')


def test_rift_abyslite_also_replaces_tuff() -> None:
    """Test abyslite alone also replaces tuff, the Primary Cave's rock below about y -250 (no ore tag holds it)."""
    for ore in _ORES:
        blocks = [target['target'].get('block') for target in _read(f'worldgen/feature/{ore}_ore.json')['targets']]
        assert ('minecraft:tuff' in blocks) == (ore == 'abyslite'), ore


def test_rift_abyslite_only_in_primary_cave() -> None:
    """Test abyslite is listed only in the Primary Cave, and the other three ores in both biomes."""
    assert 'paradox:abyslite_ore' in _features('primary_cave')
    assert 'paradox:abyslite_ore' not in _features('the_rift')
    for ore in ('eatherite', 'pirelite', 'paralite'):
        assert f'paradox:{ore}_ore' in _features('the_rift'), ore
        assert f'paradox:{ore}_ore' in _features('primary_cave'), ore


# Vanilla 26.3 placed features the Rift's biomes would list whose heights are anchored to the world's bottom
# (above_bottom, in misode/mcmeta 26.3-data-json): at the Rift's -416 floor they would sink 352 blocks.
_BOTTOM_ANCHORED = {
    # placed feature: the vanilla configured feature it places
    'ore_gravel': 'ore_gravel',
    'ore_tuff': 'ore_tuff',
    'ore_iron_small': 'ore_iron_small',
    'ore_redstone': 'ore_redstone',
    'ore_redstone_lower': 'ore_redstone',
    'ore_diamond': 'ore_diamond_small',
    'ore_diamond_large': 'ore_diamond_large',
    'ore_diamond_buried': 'ore_diamond_buried',
    'ore_lapis_buried': 'ore_lapis_buried',
}


def test_rift_features_keep_overworld_y_bands() -> None:
    """Test no listed placed feature is bottom-anchored: the pack's own use absolute y, and no vanilla one that is."""
    listed = set(_features('the_rift')) | set(_features('primary_cave'))

    assert not any('above_bottom' in path.read_text(encoding='utf-8') for path in _json_files())
    assert not {f'minecraft:{name}' for name in _BOTTOM_ANCHORED} & listed
    assert {f'paradox:{name}' for name in _BOTTOM_ANCHORED} <= listed
    for name, configured in _BOTTOM_ANCHORED.items():
        assert _read(f'worldgen/placed_feature/{name}.json')['feature'] == f'minecraft:{configured}', name


def test_rift_shared_features_keep_one_order() -> None:
    """Test the features both biomes list come in the same order in each step (no feature-order cycle)."""
    the_rift = _read('worldgen/biome/the_rift.json')['features']
    primary_cave = _read('worldgen/biome/primary_cave.json')['features']
    for step_rift, step_cave in zip(the_rift, primary_cave, strict=True):
        shared = set(step_rift) & set(step_cave)
        assert [f for f in step_rift if f in shared] == [f for f in step_cave if f in shared]


def test_rift_surface_feature_rarity() -> None:
    """Test fire mud is about one chunk in 2, and a warped clump one in 3, both on the Rift's surface."""
    fire_mud = _read('worldgen/placed_feature/fire_mud.json')
    warped_clump = _read('worldgen/placed_feature/warped_clump.json')

    assert _modifier(fire_mud, 'rarity_filter')['chance'] == 2
    assert _modifier(warped_clump, 'rarity_filter')['chance'] == 3
    assert {'paradox:fire_mud', 'paradox:warped_clump'} <= set(_features('the_rift'))


def test_rift_fire_mud_is_mud_round_a_magma_core() -> None:
    """Test the fire-mud feature lays a disk of mud, radius 2-4, then sets a magma core into it."""
    feature = _read('worldgen/feature/fire_mud.json')
    mud, core = (step['feature'] for step in feature['features'])

    assert feature['type'] == 'minecraft:sequence'
    assert mud['type'] == 'minecraft:disk'
    assert mud['state_provider'] == {'id': 'minecraft:mud'}
    assert (mud['radius']['min_inclusive'], mud['radius']['max_inclusive']) == (2, 4)
    assert core['state_provider'] == {'id': 'minecraft:magma_block'}


def test_rift_warped_clump_plants_only_on_nylium() -> None:
    """Test the clump's ground mixes nylium into wart, and its roots and sprouts are kept to the nylium."""
    feature = _read('worldgen/feature/warped_clump.json')
    ground = json.dumps(feature['ground_state'])
    vegetation = json.dumps(feature['vegetation_feature'])

    assert feature['type'] == 'minecraft:vegetation_patch'
    assert 'minecraft:warped_nylium' in ground
    assert 'minecraft:warped_wart_block' in ground
    assert 'minecraft:warped_roots' in vegetation
    assert 'minecraft:nether_sprouts' in vegetation
    assert '"blocks": "minecraft:warped_nylium"' in vegetation


def test_rift_ancient_ruin_loot_is_the_ancient_city_s() -> None:
    """Test the ruin's chest table is one pool drawing the vanilla ancient-city table."""
    table = _read('loot_table/chests/ancient_ruin.json')

    assert table['type'] == 'minecraft:chest'
    assert len(table['pools']) == 1
    assert table['pools'][0]['entries'] == [{'type': 'minecraft:loot_table', 'value': 'minecraft:chests/ancient_city'}]


def test_rift_biome_colours() -> None:
    """Test the Rift's red grass, cyan leaves and water, magenta sky, and the Primary Cave's teal fog."""
    the_rift = _read('worldgen/biome/the_rift.json')
    primary_cave = _read('worldgen/biome/primary_cave.json')

    assert the_rift['effects'] == {'foliage_color': '#7fe6e6', 'grass_color': '#b8323c', 'water_color': '#3fd0d0'}
    assert the_rift['attributes']['minecraft:visual/sky_color'] == '#5a1f45'
    assert the_rift['attributes']['minecraft:visual/fog_color'] == '#9a3a4a'
    assert primary_cave['attributes']['minecraft:visual/fog_color'] == '#0f2a2e'
    assert 'crimson_spore' in json.dumps(the_rift['attributes']['minecraft:visual/ambient_particles'])
    assert 'warped_spore' in json.dumps(primary_cave['attributes']['minecraft:visual/ambient_particles'])


# Vanilla 26.3's common overworld monsters and their weights (misode/mcmeta 26.3-data-json: the list every cave biome
# starts from; dripstone_caves adds drowned, which the dry Primary Cave leaves out).
_VANILLA_CAVE_MONSTERS = {
    'minecraft:spider': 100,
    'minecraft:zombie': 95,
    'minecraft:zombie_villager': 5,
    'minecraft:skeleton': 100,
    'minecraft:creeper': 100,
    'minecraft:slime': 100,
    'minecraft:enderman': 10,
    'minecraft:witch': 5,
}


def test_rift_primary_cave_spawns_fewer_monsters() -> None:
    """Test every Primary Cave monster has a spawn cost: weights are relative, so only spawn_costs spawn fewer."""
    spawns = _read('worldgen/biome/primary_cave.json')['attributes']['minecraft:gameplay/natural_mob_spawns']
    monsters = spawns['argument']['spawns_by_category']['monster']
    costs = spawns['argument']['spawn_costs']

    assert {entry['type']: entry['weight'] for entry in monsters} == {
        mob: weight // 2 for mob, weight in _VANILLA_CAVE_MONSTERS.items()
    }
    assert set(costs) == set(_VANILLA_CAVE_MONSTERS)
    for mob, cost in costs.items():
        assert cost == {'charge': 0.7, 'energy_budget': 0.15}, mob
