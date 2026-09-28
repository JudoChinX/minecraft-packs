# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-09-28

Initial release: the build system and its first pack.

### Added

- `enchanter` pack for Minecraft Java 26.3 (resource pack format 97). Recolours the Illusioner into a purple-robed, gold-trimmed Enchanter in the style of Minecraft Dungeons: four hue-range rules over the vanilla texture's palette turn the blue robe deep purple and its blue, teal and blue-violet speckles three tones of gold, keeping the texture's shading and transparency. The pack icon is the Enchanter's hooded face.
- `python -m minecraft_packs build` builds every pack, or the named ones, into `dist/<pack>-<version>.zip` with a `sha1sum`-format `.sha1` beside it, and prints a `RESOURCE_PACK_SHA1=` line per pack. Zips are deterministic — sorted, uncompressed entries with fixed timestamps and modes — so the same inputs give the same SHA-1 on any machine with the pinned Pillow. Each pack commits its expected SHA-1 in `expected.sha1`; `--check` fails a build that differs from it and `--update-expected` records a new one.
- `python -m minecraft_packs preview` renders a review sheet of a pack's recoloured texture and a flat front view of the model. Only the pack's derived texture is drawn, never the vanilla one.
- `python -m minecraft_packs verify` checks built zips offline: layout, `pack.mcmeta`, `pack.png`, every PNG, and the `.sha1` sidecar.
- Pack definitions in `packs/<name>/pack.toml`, validated on load with unknown keys rejected, plus an optional `files/` directory copied into the pack verbatim.
- The build downloads Mojang's official client jar into a git-ignored cache and verifies it against the SHA-1 in Mojang's manifest and the SHA-1 the pack pins, and verifies every texture against a pinned SHA-256. No Mojang files are committed; `docs/enchanter-preview.png` is a render of the pack's derived art.
- CI: lint, type, security and test checks on every push and pull request; every pack built twice and checked against its expected SHA-1; on a `v*` tag on `main`, a GitHub Release with each pack's zip and `.sha1` attached. Builds install Pillow from `requirements-hashes.txt` with `--require-hashes`.
