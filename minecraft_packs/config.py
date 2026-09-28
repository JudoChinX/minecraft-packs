"""Load and validate pack definitions: one ``packs/<name>/pack.toml`` per pack.

A pack definition is user input, so every key is checked here, once, and unknown keys are
rejected rather than ignored: a misspelt key would otherwise build a pack that silently differs
from the one intended.
"""

import re
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from minecraft_packs.errors import PackError
from minecraft_packs.models import MODELS
from minecraft_packs.recolour import Rule
from minecraft_packs.vanilla import VanillaSource

EXPECTED_SHA1_NAME = 'expected.sha1'
FILES_DIR_NAME = 'files'
PACK_FILE_NAME = 'pack.toml'

_ASSET_PATTERN = re.compile(r'^assets(/[a-z0-9_-][a-z0-9_.-]*)+\.png$')
_HUE_MAX = 360.0
_KIND_NAMES: dict[type, str] = {
    dict: 'a table',
    float: 'a number',
    int: 'an integer',
    list: 'an array',
    str: 'a string',
}
_NAME_PATTERN = re.compile(r'^[a-z0-9][a-z0-9_-]*$')
_PACK_KEYS = frozenset({'description', 'max_format', 'min_format'})
_PREVIEW_KEYS = frozenset({'model', 'texture', 'title'})
_RANGE_LENGTH = 2
_RULE_KEYS = frozenset({
    'hue',
    'lightness',
    'lightness_offset',
    'name',
    'saturation',
    'target_hue',
    'target_saturation',
})
_SHA1_PATTERN = re.compile(r'^[0-9a-f]{40}$')
_SHA256_PATTERN = re.compile(r'^[0-9a-f]{64}$')
_TABLE_KEYS = frozenset({'pack', 'preview', 'textures', 'vanilla'})
_TEXTURE_KEYS = frozenset({'path', 'rules', 'sha256'})
_UNIT_MAX = 1.0
_VANILLA_KEYS = frozenset({'client_sha1', 'version'})


@dataclass(frozen=True)
class Preview:
    """Which texture to preview, on which model layout, and what the pack calls the mob."""

    model: str
    texture: str
    title: str


@dataclass(frozen=True)
class Texture:
    """A vanilla texture the pack recolours, its pinned SHA-256, and its rules in priority order."""

    path: str
    rules: tuple[Rule, ...]
    sha256: str


@dataclass(frozen=True)
class PackConfig:
    """A validated pack definition."""

    description: str
    directory: Path
    expected_sha1: str | None
    max_format: int
    min_format: int
    name: str
    preview: Preview | None
    textures: tuple[Texture, ...]
    vanilla: VanillaSource | None

    @property
    def expected_sha1_path(self) -> Path:
        """File holding the SHA-1 the pack's zip is expected to have."""
        return self.directory / EXPECTED_SHA1_NAME

    @property
    def files_dir(self) -> Path:
        """Directory whose files are copied into the pack verbatim."""
        return self.directory / FILES_DIR_NAME

    def mcmeta(self) -> dict[str, Any]:
        """Build the ``pack.mcmeta`` document.

        Returns:
            The document, with keys in the order they are written.
        """
        return {
            'pack': {
                'description': self.description,
                'min_format': self.min_format,
                'max_format': self.max_format,
            }
        }


def _check_keys(table: dict[str, Any], allowed: frozenset[str], where: str) -> None:
    """Reject keys a table does not define."""
    unknown = sorted(set(table) - allowed)
    if unknown:
        raise PackError(f'{where}: unknown key(s) {", ".join(unknown)}; expected {", ".join(sorted(allowed))}.')


def _expected_sha1(directory: Path) -> str | None:
    """Read the SHA-1 the pack's zip is expected to have, committed beside its ``pack.toml``."""
    path = directory / EXPECTED_SHA1_NAME
    value = path.read_text(encoding='utf-8').strip() if path.is_file() else None
    if value is not None and not _SHA1_PATTERN.fullmatch(value):
        raise PackError(f'{path}: must hold one lowercase hex SHA-1, not {value!r}.')
    return value


def _field(table: dict[str, Any], key: str, kind: type, where: str) -> Any:
    """Return a required value of the given kind, rejecting booleans posing as numbers."""
    value = table.get(key)
    accepted = (int, float) if kind is float else kind
    if not isinstance(value, accepted) or isinstance(value, bool):
        raise PackError(f'{where}: {key!r} must be {_KIND_NAMES[kind]}.')
    return float(value) if kind is float else value


def _matching(table: dict[str, Any], key: str, pattern: re.Pattern[str], what: str, where: str) -> str:
    """Return a required string that must match a pattern."""
    value = _field(table, key, str, where)
    if not pattern.fullmatch(value):
        raise PackError(f'{where}: {key!r} must be {what}, not {value!r}.')
    return value


def _pack_name(directory: Path, where: str) -> str:
    """Return the pack's name, taken from its directory, which must be a safe file-name stem."""
    if not _NAME_PATTERN.fullmatch(directory.name):
        raise PackError(f'{where}: the pack directory name must use only lowercase a-z, 0-9, - and _.')
    return directory.name


def _parse_pack(document: dict[str, Any], directory: Path) -> PackConfig:
    """Build a pack definition from a parsed ``pack.toml``."""
    where = str(directory / PACK_FILE_NAME)
    _check_keys(document, _TABLE_KEYS, where)
    pack = _field(document, 'pack', dict, where)
    _check_keys(pack, _PACK_KEYS, f'{where} [pack]')
    min_format = _field(pack, 'min_format', int, f'{where} [pack]')
    max_format = _field(pack, 'max_format', int, f'{where} [pack]')
    if min_format > max_format:
        raise PackError(f'{where} [pack]: min_format {min_format} is above max_format {max_format}.')
    textures = tuple(
        _parse_texture(table, f'{where} [[textures]] #{index + 1}')
        for index, table in enumerate(_tables(document, 'textures', where))
    )
    config = PackConfig(
        description=_field(pack, 'description', str, f'{where} [pack]'),
        directory=directory,
        expected_sha1=_expected_sha1(directory),
        max_format=max_format,
        min_format=min_format,
        name=_pack_name(directory, where),
        preview=_parse_preview(document['preview'], f'{where} [preview]') if 'preview' in document else None,
        textures=textures,
        vanilla=_parse_vanilla(document['vanilla'], f'{where} [vanilla]') if 'vanilla' in document else None,
    )
    _validate_references(config, where)
    return config


def _parse_preview(table: Any, where: str) -> Preview:
    """Build the preview settings from ``[preview]``."""
    if not isinstance(table, dict):
        raise PackError(f'{where}: must be a table.')
    _check_keys(table, _PREVIEW_KEYS, where)
    model = _field(table, 'model', str, where)
    if model not in MODELS:
        raise PackError(f'{where}: unknown model {model!r}; known models: {", ".join(sorted(MODELS))}.')
    return Preview(
        model=model,
        texture=_field(table, 'texture', str, where),
        title=_field(table, 'title', str, where),
    )


def _parse_rule(table: dict[str, Any], where: str) -> Rule:
    """Build one recolour rule from a ``[[textures.rules]]`` table."""
    _check_keys(table, _RULE_KEYS, where)
    target_hue = _field(table, 'target_hue', float, where)
    target_saturation = _field(table, 'target_saturation', float, where)
    if not 0.0 <= target_hue <= _HUE_MAX or not 0.0 <= target_saturation <= _UNIT_MAX:
        raise PackError(f'{where}: target_hue must be 0-360 and target_saturation 0-1.')
    return Rule(
        hue=_range(table, 'hue', _HUE_MAX, where),
        lightness=_range(table, 'lightness', _UNIT_MAX, where),
        lightness_offset=_field(table, 'lightness_offset', float, where),
        name=_field(table, 'name', str, where),
        saturation=_range(table, 'saturation', _UNIT_MAX, where),
        target_hue=target_hue,
        target_saturation=target_saturation,
    )


def _parse_texture(table: dict[str, Any], where: str) -> Texture:
    """Build one recoloured texture from a ``[[textures]]`` table."""
    _check_keys(table, _TEXTURE_KEYS, where)
    rules = tuple(
        _parse_rule(rule, f'{where} [[textures.rules]] #{index + 1}')
        for index, rule in enumerate(_tables(table, 'rules', where))
    )
    if not rules:
        raise PackError(f'{where}: a texture needs at least one [[textures.rules]] entry.')
    return Texture(
        path=_matching(table, 'path', _ASSET_PATTERN, 'a lowercase assets/... .png path', where),
        rules=rules,
        sha256=_matching(table, 'sha256', _SHA256_PATTERN, 'a lowercase hex SHA-256', where),
    )


def _parse_vanilla(table: Any, where: str) -> VanillaSource:
    """Build the pinned vanilla release from ``[vanilla]``."""
    if not isinstance(table, dict):
        raise PackError(f'{where}: must be a table.')
    _check_keys(table, _VANILLA_KEYS, where)
    return VanillaSource(
        client_sha1=_matching(table, 'client_sha1', _SHA1_PATTERN, 'a lowercase hex SHA-1', where),
        version=_field(table, 'version', str, where),
    )


def _range(table: dict[str, Any], key: str, upper: float, where: str) -> tuple[float, float]:
    """Return an inclusive ``[low, high]`` range within ``0..upper``."""
    value = _field(table, key, list, where)
    numbers = [item for item in value if isinstance(item, int | float) and not isinstance(item, bool)]
    if len(value) != _RANGE_LENGTH or len(numbers) != _RANGE_LENGTH or not 0.0 <= numbers[0] <= numbers[1] <= upper:
        raise PackError(f'{where}: {key!r} must be [low, high] with 0 <= low <= high <= {upper:g}.')
    return float(numbers[0]), float(numbers[1])


def _tables(table: dict[str, Any], key: str, where: str) -> list[dict[str, Any]]:
    """Return an optional array of tables, empty when absent."""
    value = table.get(key, [])
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise PackError(f'{where}: {key!r} must be an array of tables ([[{key}]]).')
    return value


def _validate_references(config: PackConfig, where: str) -> None:
    """Check that the parts of a pack definition that refer to each other agree."""
    paths = [texture.path for texture in config.textures]
    if len(paths) != len(set(paths)):
        raise PackError(f'{where}: a texture path is listed more than once.')
    if paths and config.vanilla is None:
        raise PackError(f'{where}: recoloured textures need a [vanilla] release to take them from.')
    if config.preview is not None and config.preview.texture not in paths:
        raise PackError(f'{where} [preview]: texture {config.preview.texture!r} is not one of the [[textures]].')


def discover_packs(packs_dir: Path) -> list[str]:
    """List the packs defined under a directory.

    Args:
        packs_dir: The directory holding one subdirectory per pack.

    Returns:
        Sorted names of subdirectories that contain a ``pack.toml``.
    """
    return sorted(path.parent.name for path in packs_dir.glob(f'*/{PACK_FILE_NAME}'))


def load_pack(directory: Path) -> PackConfig:
    """Load and validate one pack definition.

    Args:
        directory: The pack's directory, ``packs/<name>/``.

    Returns:
        The validated pack definition.

    Raises:
        PackError: If ``pack.toml`` is missing, is not valid TOML, or fails validation.
    """
    pack_file = directory / PACK_FILE_NAME
    try:
        document = tomllib.loads(pack_file.read_text(encoding='utf-8'))
    except FileNotFoundError as error:
        raise PackError(f'{pack_file}: no such file.') from error
    except tomllib.TOMLDecodeError as error:
        raise PackError(f'{pack_file}: invalid TOML: {error}') from error
    return _parse_pack(document, directory)


def load_packs(packs_dir: Path, names: list[str]) -> list[PackConfig]:
    """Load the named packs, or every pack when no names are given.

    Args:
        packs_dir: The directory holding one subdirectory per pack.
        names: Pack names to load; empty means all of them.

    Returns:
        The validated pack definitions, in the order requested (or sorted by name).

    Raises:
        PackError: If there are no packs, or a requested pack does not exist.
    """
    available = discover_packs(packs_dir)
    if not available:
        raise PackError(f'No packs found under {packs_dir}/ (expected {packs_dir}/<name>/{PACK_FILE_NAME}).')
    unknown = [name for name in names if name not in available]
    if unknown:
        raise PackError(f'Unknown pack(s): {", ".join(unknown)}. Available: {", ".join(available)}.')
    return [load_pack(packs_dir / name) for name in names or available]
