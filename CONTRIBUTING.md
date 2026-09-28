# Contributing to Minecraft Packs

Thank you for considering contributing to Minecraft Packs! This document provides guidelines for contributing to the project and helps ensure a smooth collaboration process.

## How to Report Bugs

### General Bugs

For general bugs and feature requests, please open a GitHub issue:
- Search existing issues first to avoid duplicates.
- Provide a clear and descriptive title.
- Include steps to reproduce the issue.
- Include the command you ran and its full output.
- For a pack that looks wrong in game, include the Minecraft version, the pack's release version, and a screenshot.

### Security Vulnerabilities

**Do not open public GitHub issues for security vulnerabilities.**

Please report security issues responsibly through GitHub Security Advisories: https://github.com/JudoChinX/minecraft-packs/security/advisories/new.

See [SECURITY.md](SECURITY.md) for our full security policy and coordinated disclosure timeline.

## Development Setup

Requires Python 3.13+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
./utils/setup.sh   # installs the pre-push hook
```

## Coding Standards

All contributions must meet the following standards:

### Automated Checks

All pushes automatically run pre-push hooks (see [pre-push.sh](utils/pre-push.sh)) that enforce:

- **Ruff** (linting and formatting).
- **Pylint** (code quality).
- **Mypy** (type checking).
- **Bandit** (security scanning).
- **Yamllint** (YAML style).
- **pip-audit** (dependency vulnerabilities).
- **Pytest** (test suite, 95% coverage).

You can run these checks manually:

```bash
# Linting and formatting
ruff check .
ruff check --fix .
ruff format .

# Type checking
mypy minecraft_packs/ tests/

# Security scanning
bandit -r minecraft_packs/ -lll

# Code quality
pylint minecraft_packs/ tests/

# Run tests
pytest
pytest tests/unit/test_recolour.py -v  # Run specific test file
pytest tests/unit/test_recolour.py::test_recolour_rgb -v  # Run specific test
```

### Code Style Requirements

All submissions must pass the automated checks listed above. For coding conventions — naming, docstrings, type hints, testing patterns, and more — see the [Style Guide](docs/style-guide.md).

## Contributing a Pack

A pack is a directory under `packs/` with a `pack.toml`; see the [pack definition reference](docs/pack-definition.md).

- **Never commit Mojang's files.** No vanilla textures, no client jar, nothing extracted from it — not even as a test fixture. Changes to vanilla art are expressed as rules applied at build time. Original work (models, sounds, a hand-made icon) may go in the pack's `files/` directory. The one exception is a preview in `docs/`, which is a render of the pack's derived art.
- **Pin what you read.** Every texture a pack recolours carries the SHA-256 of the vanilla file; the build refuses a texture that does not match.
- **Show the result.** Regenerate the preview (`python -m minecraft_packs preview <pack> docs/<pack>-preview.png`) and include it in the pull request, so the change can be reviewed by eye.
- **Changing a pack changes its SHA-1.** Rebuild with `python -m minecraft_packs build --update-expected <pack>` and commit the new `packs/<pack>/expected.sha1`; CI fails a build that does not match it. Say so in the pull request and in `CHANGELOG.md`: every server pinning the old SHA-1 must be updated when it upgrades.

## Security-Conscious Contribution Guidelines

### Never Commit Sensitive Data

- **Credentials**: The build needs none. Never add a token, key or password to the repository.
- **Personal information**: No real names, emails, or identifying information in test data.
- **Built artifacts**: Never commit built zips, the client jar or the cache; they are git-ignored.

### Document Network Access

If your contribution adds or changes a download, update SECURITY.md accordingly. Every download must use HTTPS and be verified against a pinned hash.

### Add Tests for Security-Relevant Code

- Validation of pack definitions must have comprehensive test coverage, including every rejected input.
- Download verification must be tested for every way a response can disagree with a pin.
- Tests must never use the network: the root `conftest.py` blocks it, and downloads are served by the fakes in `tests/helpers.py` and `tests/builders.py`.

## Pull Request Process

### Before Creating a Pull Request

1. **Test locally**: Run the full test suite and ensure all checks pass.
2. **Update tests**: Add tests for new functionality or bug fixes.
3. **Update documentation**: Update README.md, `docs/pack-definition.md` or SECURITY.md if applicable.
4. **Review your changes**: Self-review for correctness, test coverage, and alignment with the coding standards in this file.
5. **Clean commit history**: Squash WIP commits; write clear commit messages (see [Commit Messages](#commit-messages) below).

### Creating a Pull Request

1. **Fork the repository** and create a feature branch.
2. **Push your changes** to your fork.
3. **Open a pull request** with:
   - Clear, descriptive title.
   - Summary of changes and motivation.
   - Reference to related issues (if applicable).
   - A preview image for any change to a pack's look.
4. **Respond to feedback**: Address reviewer comments promptly.

### Pull Request Expectations

- PRs will be reviewed for code quality, security, and alignment with project goals.
- All automated checks must pass before merge.
- Maintainers may request changes or additional tests.
- Large PRs may take longer to review; consider breaking into smaller PRs.
- Security-related PRs receive priority review.

## Commit Messages

Every commit message starts with a type prefix followed by a colon and a space:

| Prefix | When to use |
|---|---|
| `new:` | A new feature, pack, file, or capability that didn't exist before |
| `chg:` | A change or improvement to existing behavior, docs, or config |
| `fix:` | A bug fix |

The subject line is sentence case and must end with punctuation (a period in most cases).

```
new: Add a recolour pack for the Evoker.
chg: Deepen the Enchanter's robe by five lightness points.
fix: Keep the transparent palette entry when recolouring.
```

Keep the subject under 72 characters. If more context is needed, add a blank line followed by a body paragraph.

Squash WIP commits before opening a PR — the merged history should read as a clean sequence of meaningful changes.

## GitHub Actions

CI runs automatically on every push and pull request. The following checks must pass before a PR can be merged:

| Check | What it runs |
|---|---|
| Lint & format | `ruff check . && ruff format --check .` |
| Type checking | `mypy minecraft_packs/ tests/` |
| Code quality | `pylint minecraft_packs/ tests/` |
| Security scan | `bandit -r minecraft_packs/ -lll` |
| YAML | `yamllint .` |
| Dependency audit | `pip-audit -r requirements.txt` |
| Test suite | `pytest` (95% coverage required) |
| Reproducible build | every pack built twice with `--check`; fails unless each zip matches its `expected.sha1` |

These are the same checks run by the local pre-push hook in `utils/pre-push.sh`, apart from the reproducible build, which downloads the client jar. If CI fails on your PR, run the failing check locally to reproduce it — the output is identical.

Security-related failures (Bandit) block merge regardless of other results.

Thank you for contributing to Minecraft Packs!
