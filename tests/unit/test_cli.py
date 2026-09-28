"""Tests for cli.py and __main__.py: the build, preview and verify commands."""

import logging
import runpy
import sys
from pathlib import Path

import pytest

from minecraft_packs import __version__
from minecraft_packs.cli import main
from tests.builders import ClientJarBuilder
from tests.builders import PackBuilder
from tests.builders import ZipBuilder

_JAR = ClientJarBuilder().build()


def _source_args(tmp_path: Path) -> list[str]:
    """Build the options pointing a command at a test pack and a local client jar."""
    PackBuilder().recolouring(_JAR).build(tmp_path / 'packs')
    jar_path = ClientJarBuilder().write(tmp_path / 'client.jar')
    return [
        '--packs-dir',
        str(tmp_path / 'packs'),
        '--cache-dir',
        str(tmp_path / 'cache'),
        '--client-jar',
        str(jar_path),
    ]


def test_build(tmp_path: Path, capsys: pytest.CaptureFixture[str], caplog: pytest.LogCaptureFixture) -> None:
    """Test build prints each zip and its RESOURCE_PACK_SHA1 line, and logs the recolour counts."""
    with caplog.at_level(logging.INFO):
        status = main(['build', '--out-dir', str(tmp_path / 'dist'), *_source_args(tmp_path)])

    zip_path = tmp_path / 'dist' / f'test-{__version__}.zip'
    sha1 = (tmp_path / 'dist' / f'test-{__version__}.zip.sha1').read_text(encoding='utf-8').split()[0]
    assert status == 0
    assert capsys.readouterr().out == f'{zip_path} ({zip_path.stat().st_size} bytes)\nRESOURCE_PACK_SHA1={sha1}\n'
    assert "recoloured {'robe': 1, 'trim': 1}" in caplog.text


_build_pin_cases = {
    'check_mismatch_fails': {'options': ['--check'], 'pin': 'a' * 40, 'status': 1, 'level': 'ERROR'},
    'check_missing_fails': {'options': ['--check'], 'pin': None, 'status': 1, 'level': 'ERROR'},
    'default_mismatch_warns': {'options': [], 'pin': 'a' * 40, 'status': 0, 'level': 'WARNING'},
}


@pytest.mark.parametrize(
    'options, pin, status, level',
    [(case['options'], case['pin'], case['status'], case['level']) for case in _build_pin_cases.values()],
    ids=list(_build_pin_cases.keys()),
)
def test_build_pin_mismatch(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
    options: list[str],
    pin: str | None,
    status: int,
    level: str,
) -> None:
    """Test a zip that differs from expected.sha1 warns, or fails the build under --check."""
    source = _source_args(tmp_path)
    if pin is not None:
        (tmp_path / 'packs' / 'test' / 'expected.sha1').write_text(pin, encoding='utf-8')

    with caplog.at_level(logging.WARNING):
        result = main(['build', '--out-dir', str(tmp_path / 'dist'), *options, *source])

    assert result == status
    assert [record.levelname for record in caplog.records] == [level]
    assert 'rebuild with --update-expected' in caplog.text


def test_build_update_expected_then_check(tmp_path: Path) -> None:
    """Test --update-expected records the SHA-1, after which --check passes."""
    source = _source_args(tmp_path)
    out = ['--out-dir', str(tmp_path / 'dist')]

    assert main(['build', '--update-expected', *out, *source]) == 0

    sha1 = (tmp_path / 'dist' / f'test-{__version__}.zip.sha1').read_text(encoding='utf-8').split()[0]
    assert (tmp_path / 'packs' / 'test' / 'expected.sha1').read_text(encoding='utf-8') == f'{sha1}\n'
    assert main(['build', '--check', *out, *source]) == 0


def test_build_unknown_pack(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """Test an unknown pack name exits 1 with the error logged."""
    with caplog.at_level(logging.ERROR):
        status = main(['build', 'missing', *_source_args(tmp_path)])

    assert status == 1
    assert 'Unknown pack(s): missing. Available: test.' in caplog.text


def test_main_module(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test python -m minecraft_packs exits with main's status."""
    monkeypatch.setattr(sys, 'argv', ['minecraft_packs', 'verify', str(tmp_path / 'missing.zip')])

    with pytest.raises(SystemExit) as exit_info:
        runpy.run_module('minecraft_packs', run_name='__main__')

    assert exit_info.value.code == 1


def test_preview(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Test preview writes the review sheet and prints its path."""
    out_path = tmp_path / 'preview.png'

    status = main(['preview', 'test', str(out_path), *_source_args(tmp_path)])

    assert status == 0
    assert out_path.is_file()
    assert capsys.readouterr().out == f'{out_path}\n'


def test_verify(tmp_path: Path, capsys: pytest.CaptureFixture[str], caplog: pytest.LogCaptureFixture) -> None:
    """Test verify prints OK for a sound zip, logs problems for a broken one, and exits 1 if any failed."""
    sound = ZipBuilder().build(tmp_path / 'sound.zip')
    broken = ZipBuilder().without('pack.png').build(tmp_path / 'broken.zip')

    with caplog.at_level(logging.ERROR):
        status = main(['verify', str(sound), str(broken)])

    assert status == 1
    assert capsys.readouterr().out.startswith(f'{sound}: OK sha1=')
    assert f'{broken}: pack.png is missing' in caplog.text


def test_verify_all_sound(tmp_path: Path) -> None:
    """Test verify exits 0 when every zip is sound."""
    assert main(['verify', str(ZipBuilder().build(tmp_path / 'sound.zip'))]) == 0


def test_version(capsys: pytest.CaptureFixture[str]) -> None:
    """Test --version prints the package version."""
    with pytest.raises(SystemExit) as exit_info:
        main(['--version'])

    assert exit_info.value.code == 0
    assert capsys.readouterr().out == f'python -m minecraft_packs {__version__}\n'
