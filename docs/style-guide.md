# Minecraft Packs Style Guide

This guide codifies the code and test conventions for Minecraft Packs. It follows the same
conventions as [Rangarr](https://github.com/JudoChinX/rangarr), adapted to a build tool that
produces resource packs.

For contribution workflow (branching, pull requests, commit messages), see
[CONTRIBUTING.md](../CONTRIBUTING.md).

---

## Table of Contents

- [General Conventions](#general-conventions)
- [Naming](#naming)
- [Module Structure](#module-structure)
- [Docstrings](#docstrings)
- [Type Hints](#type-hints)
- [Error Handling](#error-handling)
- [Reproducibility](#reproducibility)
- [Testing](#testing)
- [Tooling Reference](#tooling-reference)

---

## General Conventions

### Single Quotes

All strings use single quotes. Ruff enforces this via `quote-style = "single"`. Double quotes are
permitted only when the string itself contains a single quote.

```python
# Do
label = f'{title} front'
raise PackError(f"Minecraft {version} is not in Mojang's version manifest.")

# Don't
label = f"{title} front"
```

### f-strings

Prefer f-strings over `.format()` or `%`-style interpolation, including in log calls.

```python
# Do
logger.info(f'Using cached Minecraft {source.version} client jar: {jar_path}')

# Don't
logger.info('Using cached Minecraft %s client jar: %s', source.version, jar_path)
```

### Line Length

The limit is 120 characters.

### Returns

No more than 2 `return` statements per function (pylint `max-returns = 2`). Accumulate a result,
or raise, rather than returning early a third time.

```python
# Do (from archive.py)
def _check_mcmeta(archive: zipfile.ZipFile) -> list[str]:
    """Report a missing, unreadable or incomplete ``pack.mcmeta``."""
    try:
        problem = _mcmeta_problem(json.loads(archive.read(MCMETA_NAME).decode('utf-8')))
    except KeyError:
        problem = f'{MCMETA_NAME} is missing'
    except ValueError:
        problem = f'{MCMETA_NAME} is not valid UTF-8 JSON'
    return [problem] if problem else []
```

### Variable Names

Variable names must be at least 3 characters.

```python
# Do
hue, lightness, saturation = _hls(rgb)
for row in range(result.height):
    for col in range(result.width):
        ...

# Don't
h, l, s = _hls(rgb)
for y in range(result.height):
    for x in range(result.width):
        ...
```

### Constants — No Magic Numbers or Strings

Bare numeric and string literals used as meaningful values are assigned a named constant. Module and
class-level constants are in alphabetical order. Tables of data — a model's UVs, a test's cases —
are data, not magic numbers.

```python
# Do (from render.py)
_FRONT_SCALE = 12
_TEXTURE_SCALE = 8

label = f'{title} (texture x{_TEXTURE_SCALE})'
panel = _scaled(recoloured, _TEXTURE_SCALE)

# Don't
label = f'{title} (texture x8)'
panel = _scaled(recoloured, 8)
```

### Comments

Write comments only when the WHY is non-obvious — a hidden constraint, a workaround, a subtle
invariant. Never describe what the code does.

```python
# Do — explains why a broad exception is the right one
except OSError as error:  # URLError, HTTPError and timeouts are all OSError

# Don't — describes what the code does
# Loop over the palette entries
for index in range(len(palette) // _RGB_CHANNELS):
```

### Function Ordering

Within a module, private functions (`_name`) come before public ones, and each group is sorted
alphabetically. In a class, `__init__` comes first, then private methods, then public methods, each
sorted alphabetically.

---

## Naming

| Entity | Convention | Example |
|---|---|---|
| Private function | `_snake_case` | `_check_mcmeta`, `_resolve_client` |
| Public function | `snake_case` | `build_pack`, `verify_zip` |
| Public module constant | `UPPER_CASE` | `MANIFEST_URL`, `ZIP_EPOCH` |
| Private module constant | `_UPPER_CASE` | `_RULE_KEYS`, `_TEXTURE_SCALE` |
| Class | `PascalCase` | `PackConfig`, `Rule`, `VanillaSource` |
| Type alias | `type Name = ...` | `type Rgb = tuple[int, int, int]` |
| Test case dict | `_snake_case_cases` | `_recolour_rgb_cases`, `_verify_zip_cases` |
| Builder class | `<Subject>Builder` | `PackBuilder`, `ClientJarBuilder`, `MojangBuilder` |

---

## Module Structure

Every file follows this top-to-bottom ordering:

1. Module docstring
2. Standard library imports (one per line, sorted)
3. Third-party imports (one per line, sorted)
4. Local imports (one per line, sorted)
5. Module-level type aliases and constants
6. Private functions (alphabetical)
7. Public functions and classes (interleaved alphabetically by name)
8. `if __name__ == '__main__':` guard (when present)

The isort configuration enforces `force-single-line = true` — each import is on its own line.

```python
"""Palette-preserving hue-range recolouring of textures."""

import colorsys
from dataclasses import dataclass

from PIL import Image

type Rgb = tuple[int, int, int]

_CHANNEL_MAX = 255
_DEGREES = 360
```

---

## Docstrings

### Module Docstrings

Every module starts with a docstring: one sentence for a simple module, a paragraph more when the
module holds an invariant a reader must know (see `archive.py` on why zips are stored, not deflated).

### Private Functions

Private functions get a **single-line docstring only**. No `Args:` or `Returns:` block.

```python
# Do
def _hls(rgb: Rgb) -> tuple[float, float, float]:
    """Convert an 8-bit RGB colour to HLS fractions."""
```

### Public Functions and Methods

Public functions use Google style: a summary line, then `Args:`, `Returns:`, and `Raises:` as
applicable. Omit sections that don't apply.

```python
# Do (from vanilla.py)
def read_asset(jar_path: Path, asset: str, expected_sha256: str) -> bytes:
    """Read one asset out of a client jar and check it against its pinned SHA-256.

    Args:
        jar_path: A client jar.
        asset: The asset's path inside the jar, e.g. ``assets/minecraft/textures/...png``.
        expected_sha256: The pinned SHA-256 of the asset.

    Returns:
        The asset's bytes.

    Raises:
        PackError: If the jar is unreadable, lacks the asset, or the asset has changed.
    """
```

### @override Methods

`@override` methods get **no docstring**; the base class docstring is sufficient.

### Docstring Rules

- All docstrings end with punctuation.
- Never restate the function name.
- Use double-backtick quoting for inline code references: `` ``pack.toml`` ``.

---

## Type Hints

### All Signatures Must Be Typed

Mypy enforces `disallow_untyped_defs`. Every parameter and return type is annotated, tests included.

### Type Aliases

Use the `type` keyword (PEP 695) for module-level type aliases: `type Rgb = tuple[int, int, int]`.

### Self for Fluent Builders

Builder methods return `Self` from `typing`. Never use a string annotation (`-> 'PackBuilder'`).

```python
# Do (from tests/builders.py)
def with_expected_sha1(self, text: str) -> Self:
    """Write ``text`` as the pack's ``expected.sha1``."""
    self._expected_sha1 = text
    return self
```

### @override

The `@override` decorator from `typing` is required when overriding a base class method.

### Any

Use `Any` only at true system boundaries: parsed TOML and JSON, whose shape is validated before it
is trusted, and test helpers.

---

## Error Handling

### Validate at Boundaries Only

User input and external data are validated where they enter: `pack.toml` in `config.py`, Mojang's
responses in `vanilla.py`. Internal code trusts what those boundaries return and adds no defensive
guards for states that cannot occur.

Unknown keys in a pack definition are rejected, not ignored — a misspelt key must fail the build
rather than silently produce a different pack.

### One Exception Type

Every failure a user can cause or fix raises `PackError` with a message a pack author can act on.
`cli.main()` catches it, logs it, and exits 1. Never raise a bare `Exception`, and never let a
library exception escape where a `PackError` would explain it.

```python
# Do (from vanilla.py)
except KeyError as error:
    raise PackError(f'{jar_path} has no {asset}.') from error
```

### Catch Specific Exceptions

Never use bare `except:`. Catch the specific exception type you expect.

### Downloads

Every download starts from an `https://` URL and is verified against a hash before it is used or
cached. Nothing the build downloads is trusted because of where it came from.

---

## Reproducibility

A pack's SHA-1 is its identity on every server that pins it, so any change to the bytes the build
writes is a breaking change.

- Zip entries are sorted, stored (not deflated), stamped with the zip epoch and mode 0644, with no
  directory entries. Deflating would make the SHA-1 depend on the installed zlib.
- PNGs are written with `optimize=False` by the exactly-pinned Pillow.
- Every pack commits its SHA-1 in `packs/<name>/expected.sha1`; CI builds with `--check`.
- The synthetic pack's SHA-1 is pinned in `tests/integration/test_build_pipeline.py`. If a change
  alters it, every real pack's SHA-1 changes too: update the pins deliberately, never incidentally.

---

## Testing

### Core Principles

#### 1. Absolute Isolation

The root `conftest.py` applies an `autouse` fixture to every test: `urllib.request.urlopen` and
socket connections raise `UnmockedNetworkError`. Serve downloads with `tests.helpers.serve_mojang()`
and `MojangBuilder`.

#### 2. No Mojang Files

Tests build packs from `tests/fixtures/palette-64.png`, a synthetic palette texture generated by
`utils/generate_test_fixtures.py`, inside a synthetic client jar from `ClientJarBuilder`. Never add a
Mojang asset as a fixture.

#### 3. Tiered Structure

- `tests/unit/` — fast, isolated tests, one module per source module.
- `tests/integration/` — end-to-end builds through the command line, and the pins on the shipped packs.

### Standards & Strictness

- **Warnings as Errors:** all Python warnings fail the run (`filterwarnings = error`).
- **Coverage:** a 95% coverage floor is enforced.
- **No Side Effects:** tests do not modify the filesystem outside `tmp_path`, or environment variables.

### Patterns

#### Case Dict + Parametrize Pattern

Test data lives in a module-level dict named `_<function>_cases`. Dict keys become the parametrize
`ids`. Test functions receive unpacked values, not the dict itself.

```python
_recolour_rgb_cases = {
    'grey_skin_untouched': {'rgb': (150, 150, 150), 'expected': ((150, 150, 150), None)},
    'saturated_blue_to_purple_robe': {'rgb': (40, 70, 160), 'expected': ((107, 37, 138), 'robe')},
}


@pytest.mark.parametrize(
    'rgb, expected',
    [(case['rgb'], case['expected']) for case in _recolour_rgb_cases.values()],
    ids=list(_recolour_rgb_cases.keys()),
)
def test_recolour_rgb(rgb: Rgb, expected: tuple[Rgb, str | None]) -> None:
    """Test recolour_rgb keeps shading, applies the first matching rule, and leaves others alone."""
    assert recolour_rgb(rgb, _RULES) == expected
```

#### Builder Pattern

Use the builders in `tests/builders.py` to construct pack definitions, client jars, Mojang responses
and zips. Extend them when you need something new — do not inline raw TOML, JSON or zips in tests.

```python
jar = ClientJarBuilder().build()
pack_dir = PackBuilder().recolouring(jar).with_rule_value('hue', [240, 190]).build(tmp_path)
routes = MojangBuilder(jar).with_version_sha1('0' * 40).build()
broken = ZipBuilder().without('pack.png').build(tmp_path / 'broken.zip')
```

### Conventions

- **Files:** `test_<module>.py` in `tests/unit/`; broader tests in `tests/integration/`.
- **Standalone test:** `test_<function>_<scenario>`. **Parametrized test:** `test_<function>`.
- **Log assertions:** use `caplog` with an explicit level: `with caplog.at_level(logging.INFO):`.
- **Generic data:** no real names or identifying information. Use `name = 'test'` and example hosts
  such as `https://piston-data.example/client.jar`.
- **Negative cases:** every validation and verification check has a test that makes it fire. A
  checker that never fires also reports clean.

---

## Tooling Reference

All tools run automatically via `utils/pre-push.sh` (install it with `utils/setup.sh`), and in CI.

| Tool | Purpose | Command |
|---|---|---|
| Ruff | Lint + format | `ruff check . && ruff format --check .` |
| Pylint | Code quality | `pylint minecraft_packs/ tests/` |
| Mypy | Type checking | `mypy minecraft_packs/ tests/` |
| Bandit | Security (high severity only) | `bandit -r minecraft_packs/ -lll` |
| Yamllint | YAML style | `yamllint .` |
| pip-audit | Dependency vulnerabilities | `pip-audit -r requirements.txt` |
| Pytest | Tests + 95% coverage | `pytest` |
