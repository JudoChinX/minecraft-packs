"""End-to-end builds through the command line against a fake Mojang, twice, to prove reproducibility."""

from pathlib import Path

import pytest

from minecraft_packs import __version__
from minecraft_packs.archive import verify_zip
from minecraft_packs.cli import main
from tests.builders import ClientJarBuilder
from tests.builders import MojangBuilder
from tests.builders import PackBuilder
from tests.helpers import serve_mojang

# The synthetic pack's zip SHA-1. The build must reproduce it exactly on any machine with the pinned
# Pillow; a change here means the build's output bytes changed, and every real pack's SHA-1 with it.
_GOLDEN_SHA1 = '6e83b526d75abcf74d6035d970551c10f9daa6d5'
_JAR = ClientJarBuilder().build()


def test_build_downloads_once_and_is_reproducible(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test two builds give byte-identical zips matching the pinned SHA-1, and only the first downloads."""
    PackBuilder().recolouring(_JAR).with_expected_sha1(_GOLDEN_SHA1).build(tmp_path / 'packs')
    requested = serve_mojang(monkeypatch, MojangBuilder(_JAR).build())
    source = ['--check', '--packs-dir', str(tmp_path / 'packs'), '--cache-dir', str(tmp_path / 'cache')]

    first_status = main(['build', '--out-dir', str(tmp_path / 'first'), *source])
    downloads = len(requested)
    second_status = main(['build', '--out-dir', str(tmp_path / 'second'), *source])

    name = f'test-{__version__}.zip'
    first, second = tmp_path / 'first' / name, tmp_path / 'second' / name
    assert (first_status, second_status) == (0, 0)
    assert (downloads, len(requested)) == (3, 3)
    assert first.read_bytes() == second.read_bytes()
    assert (tmp_path / 'first' / f'{name}.sha1').read_bytes() == (tmp_path / 'second' / f'{name}.sha1').read_bytes()
    assert (tmp_path / 'first' / f'{name}.sha1').read_text(encoding='utf-8').split()[0] == _GOLDEN_SHA1
    assert verify_zip(first) == []
