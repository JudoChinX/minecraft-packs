"""Fetch the official Minecraft client jar from Mojang and read verified assets out of it.

Nothing Mojang publishes is committed to this repository. The build downloads the client jar for a
pinned version into a local cache, checks it against the SHA-1 Mojang's own manifest lists and
against the SHA-1 the pack pins, and checks every asset it reads against a pinned SHA-256.
"""

import hashlib
import json
import logging
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from minecraft_packs.archive import sha1_hex
from minecraft_packs.errors import PackError

CLIENT_JAR_NAME = 'client.jar'
MANIFEST_URL = 'https://piston-meta.mojang.com/mc/game/version_manifest_v2.json'

_HTTPS_PREFIX = 'https://'
_PARTIAL_SUFFIX = '.part'
_TIMEOUT_SECONDS = 120

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class VanillaSource:
    """A pinned Minecraft release to take vanilla assets from."""

    client_sha1: str
    version: str


def _download(url: str) -> bytes:
    """Download a URL over HTTPS, refusing any other scheme."""
    if not isinstance(url, str) or not url.startswith(_HTTPS_PREFIX):
        raise PackError(f'Refusing to download {url!r}: only HTTPS URLs are fetched.')
    try:
        with urllib.request.urlopen(url, timeout=_TIMEOUT_SECONDS) as response:  # nosec B310
            data = response.read()
    except OSError as error:  # URLError, HTTPError and timeouts are all OSError
        raise PackError(f'Download failed: {url}: {error}') from error
    return data


def _parse_json(data: bytes, url: str) -> Any:
    """Parse a JSON document downloaded from ``url``."""
    try:
        document = json.loads(data)
    except ValueError as error:
        raise PackError(f'{url} did not return valid JSON: {error}') from error
    return document


def _resolve_client(version: str) -> tuple[str, str]:
    """Return the client jar URL and SHA-1 that Mojang publishes for a version."""
    manifest = _parse_json(_download(MANIFEST_URL), MANIFEST_URL)
    try:
        entries = [entry for entry in manifest['versions'] if entry['id'] == version]
        if not entries:
            raise PackError(f"Minecraft {version} is not in Mojang's version manifest.")
        version_url = entries[0]['url']
        version_data = _download(version_url)
        if sha1_hex(version_data) != entries[0]['sha1']:
            raise PackError(f'{version_url} does not match the SHA-1 the version manifest lists for it.')
        client = _parse_json(version_data, version_url)['downloads']['client']
        client_url, client_sha1 = client['url'], client['sha1']
    except (KeyError, TypeError) as error:
        raise PackError(f'Unexpected response shape from Mojang ({type(error).__name__}: {error}).') from error
    return client_url, client_sha1


def fetch_client_jar(source: VanillaSource, cache_dir: Path) -> Path:
    """Return a verified client jar for a pinned release, downloading it on a cache miss.

    A cached jar is used only if it still matches the pinned SHA-1; otherwise it is downloaded
    again. The download is written to a temporary file and moved into place, so an interrupted
    download never leaves a jar that looks complete.

    Args:
        source: The pinned release.
        cache_dir: The cache root; the jar lands in ``<cache_dir>/<version>/client.jar``.

    Returns:
        The path of the verified client jar.

    Raises:
        PackError: If Mojang lists a different SHA-1 than the pin, or the download does not match it.
    """
    jar_path = cache_dir / source.version / CLIENT_JAR_NAME
    if jar_path.is_file() and sha1_hex(jar_path.read_bytes()) == source.client_sha1:
        logger.info(f'Using cached Minecraft {source.version} client jar: {jar_path}')
        return jar_path
    client_url, listed_sha1 = _resolve_client(source.version)
    if listed_sha1 != source.client_sha1:
        raise PackError(
            f'Mojang lists client SHA-1 {listed_sha1} for Minecraft {source.version}, but the pack pins '
            f'{source.client_sha1}. Check the release before changing the pin.'
        )
    logger.info(f'Downloading the Minecraft {source.version} client jar from Mojang: {client_url}')
    data = _download(client_url)
    verify_client_jar_bytes(data, source)
    jar_path.parent.mkdir(parents=True, exist_ok=True)
    partial = jar_path.with_name(jar_path.name + _PARTIAL_SUFFIX)
    partial.write_bytes(data)
    partial.replace(jar_path)
    return jar_path


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
    try:
        with zipfile.ZipFile(jar_path) as jar:
            data = jar.read(asset)
    except (zipfile.BadZipFile, OSError) as error:
        raise PackError(f'Cannot read {jar_path}: {error}') from error
    except KeyError as error:
        raise PackError(f'{jar_path} has no {asset}.') from error
    digest = hashlib.sha256(data).hexdigest()
    if digest != expected_sha256:
        raise PackError(
            f'{asset} has SHA-256 {digest}, but the pack pins {expected_sha256}. Mojang changed it: '
            're-check the recolour rules against a fresh preview before updating the pin.'
        )
    return data


def verify_client_jar(jar_path: Path, source: VanillaSource) -> Path:
    """Check a locally supplied client jar against the pinned SHA-1.

    Args:
        jar_path: A client jar supplied by the user instead of a download.
        source: The pinned release.

    Returns:
        The same path, once verified.

    Raises:
        PackError: If the file is missing or does not match the pin.
    """
    if not jar_path.is_file():
        raise PackError(f'{jar_path}: no such file.')
    verify_client_jar_bytes(jar_path.read_bytes(), source)
    return jar_path


def verify_client_jar_bytes(data: bytes, source: VanillaSource) -> None:
    """Check client jar bytes against the pinned SHA-1.

    Args:
        data: The jar's bytes.
        source: The pinned release.

    Raises:
        PackError: If the bytes do not match the pin.
    """
    digest = sha1_hex(data)
    if digest != source.client_sha1:
        raise PackError(
            f'Client jar SHA-1 {digest} does not match the pinned {source.client_sha1} for Minecraft {source.version}.'
        )
