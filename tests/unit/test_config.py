"""Tests for config.py: loading, validating and discovering pack definitions."""

from pathlib import Path

import pytest

from minecraft_packs.config import discover_packs
from minecraft_packs.config import load_pack
from minecraft_packs.config import load_packs
from minecraft_packs.errors import PackError
from minecraft_packs.vanilla import VanillaSource
from tests.builders import TEST_VERSION
from tests.builders import ClientJarBuilder
from tests.builders import PackBuilder
from tests.helpers import FIXTURE_ASSET
from tests.helpers import sha1_of

_JAR = ClientJarBuilder().build()

_load_pack_error_cases = {
    'boolean_format': {
        'builder': PackBuilder().recolouring(_JAR).with_value('pack', 'min_format', True),
        'message': "'min_format' must be an integer",
    },
    'data_pack_with_textures': {
        'builder': PackBuilder().recolouring(_JAR).with_value('pack', 'kind', 'data'),
        'message': 'a data pack takes no [vanilla], [[textures]] or [preview]',
    },
    'kind_unknown': {
        'builder': PackBuilder().with_value('pack', 'kind', 'behaviour'),
        'message': "kind must be one of resource, data, not 'behaviour'",
    },
    'description_not_string': {
        'builder': PackBuilder().recolouring(_JAR).with_value('pack', 'description', 7),
        'message': "'description' must be a string",
    },
    'directory_name_unsafe': {
        'builder': PackBuilder().named('Test Pack'),
        'message': 'the pack directory name must use only lowercase',
    },
    'duplicate_texture': {
        'builder': PackBuilder().recolouring(_JAR).with_texture_copy(),
        'message': 'a texture path is listed more than once',
    },
    'expected_sha1_invalid': {
        'builder': PackBuilder().with_expected_sha1('not a sha1\n'),
        'message': "must hold one lowercase hex SHA-1, not 'not a sha1'",
    },
    'invalid_toml': {
        'builder': PackBuilder().with_raw_toml('[pack\n'),
        'message': 'invalid TOML',
    },
    'min_above_max': {
        'builder': PackBuilder().with_value('pack', 'min_format', 98),
        'message': 'min_format 98 is above max_format 97',
    },
    'pack_table_missing': {
        'builder': PackBuilder().without('pack'),
        'message': "'pack' must be a table",
    },
    'preview_model_unknown': {
        'builder': PackBuilder()
        .recolouring(_JAR)
        .with_table('preview', {'texture': FIXTURE_ASSET, 'model': 'zombie', 'title': 'Test'}),
        'message': "unknown model 'zombie'; known models: illager",
    },
    'preview_not_table': {
        'builder': PackBuilder().recolouring(_JAR).with_table('preview', 'illager'),
        'message': '[preview]: must be a table',
    },
    'preview_texture_not_listed': {
        'builder': PackBuilder().recolouring(_JAR).with_texture_value('path', 'assets/minecraft/textures/other.png'),
        'message': 'is not one of the [[textures]]',
    },
    'rule_key_misspelt': {
        'builder': PackBuilder().recolouring(_JAR).with_rule_value('target_heu', 10),
        'message': 'unknown key(s) target_heu',
    },
    'rule_name_missing': {
        'builder': PackBuilder().recolouring(_JAR).without_rule_value('name'),
        'message': "'name' must be a string",
    },
    'rule_range_non_numeric': {
        'builder': PackBuilder().recolouring(_JAR).with_rule_value('hue', ['a', 240]),
        'message': "'hue' must be [low, high] with 0 <= low <= high <= 360",
    },
    'rule_range_out_of_bounds': {
        'builder': PackBuilder().recolouring(_JAR).with_rule_value('saturation', [0.0, 1.5]),
        'message': "'saturation' must be [low, high] with 0 <= low <= high <= 1",
    },
    'rule_range_reversed': {
        'builder': PackBuilder().recolouring(_JAR).with_rule_value('hue', [240, 190]),
        'message': "'hue' must be [low, high]",
    },
    'rule_range_too_long': {
        'builder': PackBuilder().recolouring(_JAR).with_rule_value('lightness', [0.0, 0.5, 1.0]),
        'message': "'lightness' must be [low, high]",
    },
    'rules_missing': {
        'builder': PackBuilder().recolouring(_JAR).with_texture_value('rules', []),
        'message': 'a texture needs at least one [[textures.rules]] entry',
    },
    'target_hue_out_of_range': {
        'builder': PackBuilder().recolouring(_JAR).with_rule_value('target_hue', 400),
        'message': 'target_hue must be 0-360 and target_saturation 0-1',
    },
    'texture_path_escapes_assets': {
        'builder': PackBuilder().recolouring(_JAR).with_texture_value('path', 'assets/../pack.png'),
        'message': "'path' must be a lowercase assets/... .png path",
    },
    'texture_path_uppercase': {
        'builder': PackBuilder().recolouring(_JAR).with_texture_value('path', 'assets/minecraft/Mob.png'),
        'message': "'path' must be a lowercase assets/... .png path",
    },
    'texture_sha256_invalid': {
        'builder': PackBuilder().recolouring(_JAR).with_texture_value('sha256', 'F' * 64),
        'message': "'sha256' must be a lowercase hex SHA-256",
    },
    'textures_not_tables': {
        'builder': PackBuilder().with_table('textures', ['illusioner.png']),
        'message': "'textures' must be an array of tables",
    },
    'textures_without_vanilla': {
        'builder': PackBuilder().recolouring(_JAR).without('vanilla').without('preview'),
        'message': 'recoloured textures need a [vanilla] release',
    },
    'top_level_key_unknown': {
        'builder': PackBuilder().with_table('extra', {'key': 'value'}),
        'message': 'unknown key(s) extra; expected pack, preview, textures, vanilla',
    },
    'vanilla_key_unknown': {
        'builder': PackBuilder().recolouring(_JAR).with_value('vanilla', 'jar_sha1', 'x'),
        'message': 'unknown key(s) jar_sha1',
    },
    'vanilla_not_table': {
        'builder': PackBuilder().recolouring(_JAR).with_table('vanilla', TEST_VERSION),
        'message': '[vanilla]: must be a table',
    },
    'vanilla_sha1_invalid': {
        'builder': PackBuilder().recolouring(_JAR).with_value('vanilla', 'client_sha1', 'abc'),
        'message': "'client_sha1' must be a lowercase hex SHA-1",
    },
}


def test_discover_packs(tmp_path: Path) -> None:
    """Test only subdirectories holding a pack.toml are packs, listed by name."""
    PackBuilder('zeta').build(tmp_path)
    PackBuilder('alpha').build(tmp_path)
    (tmp_path / 'notes').mkdir()

    assert discover_packs(tmp_path) == ['alpha', 'zeta']


def test_load_pack_expected_sha1(tmp_path: Path) -> None:
    """Test a committed expected.sha1 is read, surrounding whitespace ignored."""
    pack = load_pack(PackBuilder().with_expected_sha1(f'{"a" * 40}\n').build(tmp_path))

    assert pack.expected_sha1 == 'a' * 40
    assert pack.expected_sha1_path == tmp_path / 'test' / 'expected.sha1'


def test_load_pack_minimal(tmp_path: Path) -> None:
    """Test a pack with only [pack] loads, with no textures, preview or vanilla release."""
    pack = load_pack(PackBuilder().build(tmp_path))

    assert (pack.name, pack.textures, pack.preview, pack.vanilla, pack.expected_sha1) == ('test', (), None, None, None)
    assert pack.files_dir == tmp_path / 'test' / 'files'


def test_load_pack_recolouring(tmp_path: Path) -> None:
    """Test a full definition loads, with ranges and targets as floats and rules in order."""
    pack = load_pack(PackBuilder().recolouring(_JAR).build(tmp_path))

    assert pack.vanilla == VanillaSource(client_sha1=sha1_of(_JAR), version=TEST_VERSION)
    assert pack.preview is not None and pack.preview.model == 'illager'
    assert [rule.name for rule in pack.textures[0].rules] == ['robe', 'trim']
    assert pack.textures[0].rules[0].hue == (190.0, 240.0)
    assert pack.textures[0].rules[0].target_hue == 282.0


@pytest.mark.parametrize(
    'builder, message',
    [(case['builder'], case['message']) for case in _load_pack_error_cases.values()],
    ids=list(_load_pack_error_cases.keys()),
)
def test_load_pack_errors(tmp_path: Path, builder: PackBuilder, message: str) -> None:
    """Test every invalid definition is rejected with a message naming the problem."""
    directory = builder.build(tmp_path)

    with pytest.raises(PackError) as error:
        load_pack(directory)

    assert message in str(error.value)


def test_load_pack_missing(tmp_path: Path) -> None:
    """Test a directory without a pack.toml is reported."""
    with pytest.raises(PackError, match='no such file'):
        load_pack(tmp_path)


def test_load_packs_all_by_default(tmp_path: Path) -> None:
    """Test no names loads every pack, sorted by name."""
    PackBuilder('zeta').build(tmp_path)
    PackBuilder('alpha').build(tmp_path)

    assert [pack.name for pack in load_packs(tmp_path, [])] == ['alpha', 'zeta']


def test_load_packs_named(tmp_path: Path) -> None:
    """Test named packs load in the order requested."""
    PackBuilder('zeta').build(tmp_path)
    PackBuilder('alpha').build(tmp_path)

    assert [pack.name for pack in load_packs(tmp_path, ['zeta', 'alpha'])] == ['zeta', 'alpha']


def test_load_packs_none(tmp_path: Path) -> None:
    """Test a directory with no packs is an error, not an empty build."""
    with pytest.raises(PackError, match='No packs found'):
        load_packs(tmp_path, [])


def test_load_packs_unknown(tmp_path: Path) -> None:
    """Test an unknown pack name is reported with the packs that do exist."""
    PackBuilder('alpha').build(tmp_path)

    with pytest.raises(PackError, match='Unknown pack\\(s\\): beta. Available: alpha.'):
        load_packs(tmp_path, ['beta'])


def test_mcmeta_key_order(tmp_path: Path) -> None:
    """Test pack.mcmeta keys are written description first, then the format range."""
    pack = load_pack(PackBuilder().build(tmp_path))

    assert list(pack.mcmeta()['pack']) == ['description', 'min_format', 'max_format']
