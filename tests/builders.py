"""Test data builders for pack definitions, client jars, Mojang responses and pack zips."""

import copy
import io
import json
import zipfile
from pathlib import Path
from typing import Any
from typing import Self

from PIL import Image

from minecraft_packs.archive import ZIP_EPOCH
from minecraft_packs.recolour import Rule
from minecraft_packs.vanilla import MANIFEST_URL
from tests.helpers import FIXTURE_ASSET
from tests.helpers import fixture_bytes
from tests.helpers import sha1_of
from tests.helpers import sha256_of
from tests.helpers import to_toml

TEST_VERSION = '1.0'


class ClientJarBuilder:
    """Builder for a synthetic client jar holding the fixture texture."""

    def __init__(self) -> None:
        """Start with the fixture texture at ``FIXTURE_ASSET``."""
        self._assets: dict[str, bytes] = {FIXTURE_ASSET: fixture_bytes()}

    def build(self) -> bytes:
        """Build the jar's bytes, identical on every call."""
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as jar:
            for name in sorted(self._assets):
                jar.writestr(zipfile.ZipInfo(name, ZIP_EPOCH), self._assets[name])
        return buffer.getvalue()

    def with_asset(self, name: str, data: bytes) -> Self:
        """Add or replace an asset."""
        self._assets[name] = data
        return self

    def write(self, path: Path) -> Path:
        """Write the jar to a file and return its path."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(self.build())
        return path


class MojangBuilder:
    """Builder for the fake responses of Mojang's manifest, version JSON and client download."""

    def __init__(self, jar: bytes) -> None:
        """Serve ``jar`` as the client for ``TEST_VERSION``, with consistent hashes throughout."""
        self._client_sha1 = sha1_of(jar)
        self._client_url = 'https://piston-data.example/client.jar'
        self._jar: bytes | Exception = jar
        self._manifest: bytes | None = None
        self._version_id = TEST_VERSION
        self._version_sha1: str | None = None
        self._version_url = 'https://piston-meta.example/version.json'

    def build(self) -> dict[str, bytes | Exception]:
        """Build the routes: response bytes (or an exception) keyed by URL."""
        version_json = json.dumps({'downloads': {'client': {'sha1': self._client_sha1, 'url': self._client_url}}})
        version_bytes = version_json.encode()
        entry = {'id': self._version_id, 'sha1': self._version_sha1 or sha1_of(version_bytes), 'url': self._version_url}
        manifest = self._manifest or json.dumps({'versions': [entry]}).encode()
        return {MANIFEST_URL: manifest, self._version_url: version_bytes, self._client_url: self._jar}

    def listing_client_sha1(self, sha1: str) -> Self:
        """Make the version JSON list a different client SHA-1."""
        self._client_sha1 = sha1
        return self

    def serving_jar(self, jar: bytes | Exception) -> Self:
        """Serve different jar bytes, or raise an exception, for the client download."""
        self._jar = jar
        return self

    def with_client_url(self, url: str) -> Self:
        """List a different client download URL."""
        self._client_url = url
        return self

    def with_manifest(self, manifest: bytes) -> Self:
        """Serve a raw manifest instead of the generated one."""
        self._manifest = manifest
        return self

    def with_version_id(self, version_id: str) -> Self:
        """List the version under a different id."""
        self._version_id = version_id
        return self

    def with_version_sha1(self, sha1: str) -> Self:
        """Make the manifest list a wrong SHA-1 for the version JSON."""
        self._version_sha1 = sha1
        return self


class PackBuilder:
    """Builder for a pack directory: ``<parent>/<name>/pack.toml`` and optional ``files/``."""

    def __init__(self, name: str = 'test') -> None:
        """Start with a minimal pack: a description and formats, nothing else."""
        self._document: dict[str, Any] = {
            'pack': {'description': 'Test pack', 'min_format': 97, 'max_format': 97},
        }
        self._expected_sha1: str | None = None
        self._files: dict[str, bytes] = {}
        self._name = name
        self._raw: str | None = None

    def build(self, parent: Path) -> Path:
        """Write the pack under ``parent`` and return its directory."""
        directory = parent / self._name
        directory.mkdir(parents=True, exist_ok=True)
        (directory / 'pack.toml').write_text(self._raw or to_toml(self._document), encoding='utf-8')
        if self._expected_sha1 is not None:
            (directory / 'expected.sha1').write_text(self._expected_sha1, encoding='utf-8')
        for name, data in self._files.items():
            target = directory / 'files' / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        return directory

    def named(self, name: str) -> Self:
        """Set the pack's directory name."""
        self._name = name
        return self

    def recolouring(self, jar: bytes) -> Self:
        """Recolour the fixture texture from ``jar``, with a preview and the default rule set."""
        self._document['vanilla'] = {'version': TEST_VERSION, 'client_sha1': sha1_of(jar)}
        self._document['preview'] = {'texture': FIXTURE_ASSET, 'model': 'illager', 'title': 'Test'}
        self._document['textures'] = [
            {
                'path': FIXTURE_ASSET,
                'sha256': sha256_of(fixture_bytes()),
                'rules': [RuleBuilder().robe().build_table(), RuleBuilder().trim().build_table()],
            }
        ]
        return self

    def with_expected_sha1(self, text: str) -> Self:
        """Write ``text`` as the pack's ``expected.sha1``."""
        self._expected_sha1 = text
        return self

    def with_file(self, name: str, data: bytes) -> Self:
        """Add a file under ``files/``, copied into the pack verbatim."""
        self._files[name] = data
        return self

    def with_raw_toml(self, text: str) -> Self:
        """Write ``text`` as ``pack.toml`` instead of the built document."""
        self._raw = text
        return self

    def with_rule_value(self, key: str, value: Any) -> Self:
        """Set a key on the first texture's first rule."""
        self._document['textures'][0]['rules'][0][key] = value
        return self

    def with_table(self, key: str, value: Any) -> Self:
        """Set a top-level key or table."""
        self._document[key] = value
        return self

    def with_texture_copy(self) -> Self:
        """List the first texture a second time."""
        self._document['textures'].append(copy.deepcopy(self._document['textures'][0]))
        return self

    def with_texture_value(self, key: str, value: Any) -> Self:
        """Set a key on the first texture."""
        self._document['textures'][0][key] = value
        return self

    def with_value(self, table: str, key: str, value: Any) -> Self:
        """Set a key in a top-level table."""
        self._document[table][key] = value
        return self

    def without(self, table: str, key: str | None = None) -> Self:
        """Remove a top-level table, or one key from it."""
        if key is None:
            del self._document[table]
        else:
            del self._document[table][key]
        return self

    def without_rule_value(self, key: str) -> Self:
        """Remove a key from the first texture's first rule."""
        del self._document['textures'][0]['rules'][0][key]
        return self


class RuleBuilder:
    """Builder for recolour rules, as TOML tables or as ``Rule`` objects."""

    def __init__(self) -> None:
        """Start with a rule that matches every colour and turns it purple."""
        self._data: dict[str, Any] = {
            'name': 'all',
            'hue': [0, 360],
            'saturation': [0.0, 1.0],
            'lightness': [0.0, 1.0],
            'target_hue': 282,
            'target_saturation': 0.58,
            'lightness_offset': 0.0,
        }

    def _set(
        self,
        name: str,
        hue: tuple[float, float],
        saturation: tuple[float, float],
        lightness: tuple[float, float],
        target: tuple[float, float, float],
    ) -> Self:
        """Set every field at once from ranges and a (hue, saturation, lightness offset) target."""
        self._data = {
            'name': name,
            'hue': list(hue),
            'saturation': list(saturation),
            'lightness': list(lightness),
            'target_hue': target[0],
            'target_saturation': target[1],
            'lightness_offset': target[2],
        }
        return self

    def amber(self) -> Self:
        """Teal to amber gold."""
        return self._set('amber', (150, 190), (0.30, 1.00), (0.00, 1.00), (38, 0.80, 0.12))

    def build(self) -> Rule:
        """Build a ``Rule``."""
        data = self._data
        return Rule(
            hue=(float(data['hue'][0]), float(data['hue'][1])),
            lightness=(float(data['lightness'][0]), float(data['lightness'][1])),
            lightness_offset=float(data['lightness_offset']),
            name=data['name'],
            saturation=(float(data['saturation'][0]), float(data['saturation'][1])),
            target_hue=float(data['target_hue']),
            target_saturation=float(data['target_saturation']),
        )

    def build_table(self) -> dict[str, Any]:
        """Build the rule as a ``[[textures.rules]]`` table."""
        return copy.deepcopy(self._data)

    def named(self, name: str) -> Self:
        """Set the rule's name."""
        self._data['name'] = name
        return self

    def pale(self) -> Self:
        """Blue-violet to pale gold."""
        return self._set('pale', (240, 275), (0.20, 1.00), (0.00, 1.00), (52, 0.75, 0.24))

    def robe(self) -> Self:
        """Saturated blue to deep violet-purple."""
        return self._set('robe', (190, 240), (0.40, 1.00), (0.00, 1.00), (282, 0.58, -0.05))

    def trim(self) -> Self:
        """Pale blue to gold."""
        return self._set('trim', (190, 240), (0.10, 0.40), (0.45, 1.00), (45, 0.85, 0.06))


class ZipBuilder:
    """Builder for pack zips written exactly as specified, including broken ones."""

    def __init__(self) -> None:
        """Start with a sound pack: a valid ``pack.mcmeta`` and a 64 x 64 ``pack.png``."""
        self._entries: list[tuple[zipfile.ZipInfo, bytes]] = []
        self._reversed = False
        self.with_mcmeta({'pack': {'description': 'Test pack', 'min_format': 97, 'max_format': 97}})
        self.with_png('pack.png', (64, 64))

    def build(self, path: Path) -> Path:
        """Write the zip, entries sorted by name (or reverse-sorted), and return its path."""
        entries = sorted(self._entries, key=lambda entry: entry[0].filename, reverse=self._reversed)
        with zipfile.ZipFile(path, 'w') as archive:
            for info, data in entries:
                archive.writestr(info, data)
        return path

    def unsorted(self) -> Self:
        """Write the entries in reverse name order."""
        self._reversed = True
        return self

    def with_entry(
        self,
        name: str,
        data: bytes,
        date_time: tuple[int, int, int, int, int, int] = ZIP_EPOCH,
        mode: int = 0o100644,
        compress_type: int = zipfile.ZIP_STORED,
    ) -> Self:
        """Add an entry with a timestamp, mode and compression, replacing any entry of the same name."""
        info = zipfile.ZipInfo(name, date_time)
        info.external_attr = mode << 16
        info.compress_type = compress_type
        self._entries = [entry for entry in self._entries if entry[0].filename != name]
        self._entries.append((info, data))
        return self

    def with_mcmeta(self, document: Any) -> Self:
        """Set ``pack.mcmeta`` to a JSON document."""
        return self.with_entry('pack.mcmeta', json.dumps(document).encode())

    def with_png(self, name: str, size: tuple[int, int]) -> Self:
        """Add a blank RGBA PNG of the given size."""
        buffer = io.BytesIO()
        Image.new('RGBA', size).save(buffer, format='PNG')
        return self.with_entry(name, buffer.getvalue())

    def without(self, name: str) -> Self:
        """Remove an entry."""
        self._entries = [entry for entry in self._entries if entry[0].filename != name]
        return self
