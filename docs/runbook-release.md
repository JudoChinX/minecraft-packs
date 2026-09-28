# Runbook: Cutting a Release

Step-by-step process for tagging and publishing a new release of the packs.

---

## Overview

Pushing a `v*` tag that points at a commit on `main` triggers the CI/CD pipeline, which:

1. Runs the full test and quality suite
2. Builds every pack twice and fails unless both builds are byte-identical
3. Checks the tag is on `main` and matches the package version
4. Builds and verifies every pack, and creates a GitHub Release with release notes extracted from
   `CHANGELOG.md`, attaching each `<pack>-<version>.zip` and its `.sha1`

Every pack shares the repository's version. A release whose packs did not change still produces
zips with the same SHA-1s as before, under new names.

---

## Pre-flight Checks

Before cutting a release, confirm:

- [ ] All intended changes are merged to `main`
- [ ] Any change to a pack's look has a regenerated preview in `docs/`, reviewed, and a committed
      `packs/<pack>/expected.sha1` (`python -m minecraft_packs build --update-expected <pack>`)
- [ ] `CHANGELOG.md` `[Unreleased]` is empty: its entries moved into a `[X.Y.Z] - YYYY-MM-DD` section
- [ ] The version follows [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`

---

## Steps

### 1. Bump the version

On a `release-vX.Y.Z` branch, set the same version in both places (a test fails if they disagree):

- `pyproject.toml` — `version = "X.Y.Z"`
- `minecraft_packs/__init__.py` — `__version__ = 'X.Y.Z'`

Move the `[Unreleased]` entries in `CHANGELOG.md` into a new `## [X.Y.Z] - YYYY-MM-DD` section and
leave `[Unreleased]` empty.

### 2. Build locally and note the SHA-1s

```bash
python -m minecraft_packs build --check
```

`--check` fails unless every zip matches its committed `expected.sha1`. The release job runs the same
build with the same check, so the `.sha1` assets it publishes equal the committed pins.

### 3. Merge, then tag `main`

Commit (`new: Minecraft Packs vX.Y.Z release.`), open a pull request, and merge it once CI is
green. Then tag the merge commit on `main` and push the tag:

```bash
git checkout main && git pull --ff-only
git tag vX.Y.Z
git push origin vX.Y.Z
```

### 4. Confirm the release

- The release exists at `https://github.com/JudoChinX/minecraft-packs/releases/tag/vX.Y.Z`
- Each `<pack>-X.Y.Z.zip` has a `<pack>-X.Y.Z.zip.sha1` beside it
- `python -m minecraft_packs verify` passes on the downloaded zip, and `sha1sum -c` passes on its
  sidecar

### 5. Update servers

Point each server's resource pack URL at the new release asset and set its SHA-1 from the matching
`.sha1`, in the same change.

---

## If the Release Job Fails

- **Tag is not on `main`:** delete the tag (`git push --delete origin vX.Y.Z`), then tag the commit
  on `main`.
- **Tag does not match the package version:** fix the version on `main`, delete and re-create the tag.
- **Mojang download failed:** re-run the job; the build is idempotent.
