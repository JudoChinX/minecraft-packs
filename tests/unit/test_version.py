"""Tests that the package version, pyproject.toml, CHANGELOG.md and the requirements files agree."""

import re
import tomllib

from minecraft_packs import __version__
from tests.helpers import REPO_ROOT


def test_changelog_has_version_section() -> None:
    """Test CHANGELOG.md has a section for the current version, so a release has notes."""
    changelog = (REPO_ROOT / 'CHANGELOG.md').read_text(encoding='utf-8')

    assert f'## [{__version__}] - ' in changelog


def test_pyproject_version_matches_package() -> None:
    """Test pyproject.toml and minecraft_packs.__version__ carry the same version."""
    pyproject = tomllib.loads((REPO_ROOT / 'pyproject.toml').read_text(encoding='utf-8'))

    assert pyproject['project']['version'] == __version__


def test_requirements_pin_the_same_pillow() -> None:
    """Test pyproject.toml and requirements-hashes.txt, used by CI's builds, pin the Pillow of requirements.txt."""
    plain = (REPO_ROOT / 'requirements.txt').read_text(encoding='utf-8').split()
    hashed = (REPO_ROOT / 'requirements-hashes.txt').read_text(encoding='utf-8')
    pyproject = tomllib.loads((REPO_ROOT / 'pyproject.toml').read_text(encoding='utf-8'))

    assert len(plain) == 1
    assert pyproject['project']['dependencies'] == plain
    assert re.search(rf'^{re.escape(plain[0])} \\$', hashed, re.MULTILINE)
    assert '--hash=sha256:' in hashed
