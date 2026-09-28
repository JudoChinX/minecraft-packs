"""Tests for vanilla.py: fetching and caching the client jar, and reading verified assets."""

from pathlib import Path

import pytest

from minecraft_packs.errors import PackError
from minecraft_packs.vanilla import MANIFEST_URL
from minecraft_packs.vanilla import VanillaSource
from minecraft_packs.vanilla import _download
from minecraft_packs.vanilla import fetch_client_jar
from minecraft_packs.vanilla import read_asset
from minecraft_packs.vanilla import verify_client_jar
from tests.builders import TEST_VERSION
from tests.builders import ClientJarBuilder
from tests.builders import MojangBuilder
from tests.helpers import FIXTURE_ASSET
from tests.helpers import fixture_bytes
from tests.helpers import serve_mojang
from tests.helpers import sha1_of
from tests.helpers import sha256_of
from tests.helpers import url_error

_JAR = ClientJarBuilder().build()
_SOURCE = VanillaSource(client_sha1=sha1_of(_JAR), version=TEST_VERSION)

_fetch_client_jar_error_cases = {
    'client_url_not_https': {
        'routes': MojangBuilder(_JAR).with_client_url('http://piston-data.example/client.jar').build(),
        'message': "Refusing to download 'http://piston-data.example/client.jar'",
    },
    'download_does_not_match_pin': {
        'routes': MojangBuilder(_JAR).serving_jar(b'tampered').build(),
        'message': f'does not match the pinned {sha1_of(_JAR)}',
    },
    'manifest_lists_another_client': {
        'routes': MojangBuilder(_JAR).listing_client_sha1('0' * 40).build(),
        'message': f'Mojang lists client SHA-1 {"0" * 40} for Minecraft {TEST_VERSION}',
    },
    'manifest_not_json': {
        'routes': MojangBuilder(_JAR).with_manifest(b'<html>').build(),
        'message': f'{MANIFEST_URL} did not return valid JSON',
    },
    'manifest_wrong_shape': {
        'routes': MojangBuilder(_JAR).with_manifest(b'{"latest": {}}').build(),
        'message': "Unexpected response shape from Mojang (KeyError: 'versions')",
    },
    'network_error': {
        'routes': MojangBuilder(_JAR).serving_jar(url_error('connection refused')).build(),
        'message': 'Download failed: https://piston-data.example/client.jar',
    },
    'version_json_tampered': {
        'routes': MojangBuilder(_JAR).with_version_sha1('0' * 40).build(),
        'message': 'does not match the SHA-1 the version manifest lists for it',
    },
    'version_not_listed': {
        'routes': MojangBuilder(_JAR).with_version_id('0.9').build(),
        'message': f"Minecraft {TEST_VERSION} is not in Mojang's version manifest",
    },
}

_read_asset_error_cases = {
    'asset_changed': {
        'jar': ClientJarBuilder().with_asset(FIXTURE_ASSET, b'changed'),
        'message': f'the pack pins {sha256_of(fixture_bytes())}. Mojang changed it',
    },
    'asset_missing': {
        'jar': ClientJarBuilder().with_asset('assets/other.png', b'x'),
        'asset': 'assets/missing.png',
        'message': 'has no assets/missing.png',
    },
}


def test_download_rejects_non_string_url() -> None:
    """Test a URL of the wrong type from a manifest is refused rather than fetched."""
    with pytest.raises(PackError, match='only HTTPS URLs are fetched'):
        _download(None)  # type: ignore[arg-type]


def test_fetch_client_jar_downloads_and_caches(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a cache miss resolves the client through the manifest, verifies it and caches it."""
    requested = serve_mojang(monkeypatch, MojangBuilder(_JAR).build())

    jar_path = fetch_client_jar(_SOURCE, tmp_path)

    assert jar_path == tmp_path / TEST_VERSION / 'client.jar'
    assert jar_path.read_bytes() == _JAR
    assert requested == [
        MANIFEST_URL,
        'https://piston-meta.example/version.json',
        'https://piston-data.example/client.jar',
    ]
    assert list(jar_path.parent.iterdir()) == [jar_path]


@pytest.mark.parametrize(
    'routes, message',
    [(case['routes'], case['message']) for case in _fetch_client_jar_error_cases.values()],
    ids=list(_fetch_client_jar_error_cases.keys()),
)
def test_fetch_client_jar_errors(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    routes: dict[str, bytes | Exception],
    message: str,
) -> None:
    """Test every way Mojang's responses can disagree with the pin fails the build and caches nothing."""
    serve_mojang(monkeypatch, routes)

    with pytest.raises(PackError) as error:
        fetch_client_jar(_SOURCE, tmp_path)

    assert message in str(error.value)
    assert not (tmp_path / TEST_VERSION / 'client.jar').exists()


def test_fetch_client_jar_redownloads_stale_cache(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a cached jar that no longer matches the pin is replaced, not trusted."""
    ClientJarBuilder().with_asset('assets/stale.png', b'x').write(tmp_path / TEST_VERSION / 'client.jar')
    requested = serve_mojang(monkeypatch, MojangBuilder(_JAR).build())

    jar_path = fetch_client_jar(_SOURCE, tmp_path)

    assert jar_path.read_bytes() == _JAR
    assert len(requested) == 3


def test_fetch_client_jar_uses_valid_cache_offline(tmp_path: Path) -> None:
    """Test a cached jar matching the pin is used without touching the network."""
    cached = ClientJarBuilder().write(tmp_path / TEST_VERSION / 'client.jar')

    assert fetch_client_jar(_SOURCE, tmp_path) == cached


def test_read_asset(tmp_path: Path) -> None:
    """Test an asset matching its pinned SHA-256 is returned."""
    jar_path = ClientJarBuilder().write(tmp_path / 'client.jar')

    assert read_asset(jar_path, FIXTURE_ASSET, sha256_of(fixture_bytes())) == fixture_bytes()


@pytest.mark.parametrize(
    'jar, asset, message',
    [(case['jar'], case.get('asset', FIXTURE_ASSET), case['message']) for case in _read_asset_error_cases.values()],
    ids=list(_read_asset_error_cases.keys()),
)
def test_read_asset_errors(tmp_path: Path, jar: ClientJarBuilder, asset: str, message: str) -> None:
    """Test a missing or changed asset fails with an explanation."""
    jar_path = jar.write(tmp_path / 'client.jar')

    with pytest.raises(PackError, match=message):
        read_asset(jar_path, asset, sha256_of(fixture_bytes()))


def test_read_asset_unreadable_jar(tmp_path: Path) -> None:
    """Test a jar that is not a zip fails with an explanation."""
    jar_path = tmp_path / 'client.jar'
    jar_path.write_bytes(b'not a jar')

    with pytest.raises(PackError, match='Cannot read'):
        read_asset(jar_path, FIXTURE_ASSET, sha256_of(fixture_bytes()))


def test_verify_client_jar(tmp_path: Path) -> None:
    """Test a local jar matching the pin is accepted."""
    jar_path = ClientJarBuilder().write(tmp_path / 'client.jar')

    assert verify_client_jar(jar_path, _SOURCE) == jar_path


def test_verify_client_jar_missing(tmp_path: Path) -> None:
    """Test a local jar that does not exist is reported."""
    with pytest.raises(PackError, match='no such file'):
        verify_client_jar(tmp_path / 'client.jar', _SOURCE)


def test_verify_client_jar_mismatch(tmp_path: Path) -> None:
    """Test a local jar that differs from the pin is refused."""
    jar_path = ClientJarBuilder().with_asset('assets/extra.png', b'x').write(tmp_path / 'client.jar')

    with pytest.raises(PackError, match=f'does not match the pinned {_SOURCE.client_sha1}'):
        verify_client_jar(jar_path, _SOURCE)
