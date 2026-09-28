"""Shared test helpers: fixture access, hashing, TOML writing and a fake Mojang download server."""

import hashlib
import io
import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import pytest

from tests.conftest import UnmockedNetworkError

FIXTURE_ASSET = 'assets/minecraft/textures/entity/test/mob.png'
FIXTURE_PATH = Path(__file__).parent / 'fixtures' / 'palette-64.png'
REPO_ROOT = Path(__file__).parent.parent


def _is_table(value: Any) -> bool:
    """Report whether a value is written as a TOML table."""
    return isinstance(value, dict)


def _is_table_array(value: Any) -> bool:
    """Report whether a value is written as a TOML array of tables."""
    return isinstance(value, list) and bool(value) and all(isinstance(item, dict) for item in value)


def _write_table(table: dict[str, Any], prefix: str, lines: list[str]) -> None:
    """Append a table's scalars, then its sub-tables and arrays of tables, as TOML lines."""
    for key, value in table.items():
        if not _is_table(value) and not _is_table_array(value):
            lines.append(f'{key} = {json.dumps(value, ensure_ascii=False)}')
    for key, value in table.items():
        if _is_table(value):
            lines.extend(['', f'[{prefix}{key}]'])
            _write_table(value, f'{prefix}{key}.', lines)
    for key, value in table.items():
        if _is_table_array(value):
            for item in value:
                lines.extend(['', f'[[{prefix}{key}]]'])
                _write_table(item, f'{prefix}{key}.', lines)


def fixture_bytes() -> bytes:
    """Return the synthetic palette texture's bytes.

    Returns:
        The PNG bytes of ``tests/fixtures/palette-64.png``.
    """
    return FIXTURE_PATH.read_bytes()


def serve_mojang(monkeypatch: pytest.MonkeyPatch, routes: dict[str, bytes | Exception]) -> list[str]:
    """Replace ``urlopen`` with a fake that serves fixed responses.

    Args:
        monkeypatch: The test's monkeypatch fixture.
        routes: Response bytes, or an exception to raise, keyed by URL.

    Returns:
        A list that records every URL requested, in order.
    """
    requested: list[str] = []

    def fake_urlopen(url: str, timeout: float) -> io.BytesIO:
        requested.append(url)
        if url not in routes:
            raise UnmockedNetworkError(f'No fake route for {url} (timeout {timeout}).')
        response = routes[url]
        if isinstance(response, Exception):
            raise response
        return io.BytesIO(response)

    monkeypatch.setattr(urllib.request, 'urlopen', fake_urlopen)
    return requested


def sha1_of(data: bytes) -> str:
    """Return the SHA-1 of bytes.

    Args:
        data: The bytes to hash.

    Returns:
        The lowercase hexadecimal digest.
    """
    return hashlib.sha1(data, usedforsecurity=False).hexdigest()


def sha256_of(data: bytes) -> str:
    """Return the SHA-256 of bytes.

    Args:
        data: The bytes to hash.

    Returns:
        The lowercase hexadecimal digest.
    """
    return hashlib.sha256(data).hexdigest()


def to_toml(document: dict[str, Any]) -> str:
    """Write a document as TOML, enough for pack definitions.

    Scalars and arrays are written as JSON literals, which TOML accepts for strings, numbers,
    booleans and arrays.

    Args:
        document: Nested tables, arrays of tables, and scalar values.

    Returns:
        The TOML text.
    """
    lines: list[str] = []
    _write_table(document, '', lines)
    return '\n'.join(lines) + '\n'


def url_error(reason: str) -> urllib.error.URLError:
    """Build the error ``urlopen`` raises when a host cannot be reached.

    Args:
        reason: The failure reason.

    Returns:
        A URLError to serve in place of a response.
    """
    return urllib.error.URLError(reason)
