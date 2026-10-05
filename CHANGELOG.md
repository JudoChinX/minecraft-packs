# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.9.0] - 2026-10-05

Daxton's seventh batch of mobs.

### Added

- `mobs` pack: one item, the Ancient Callings (`mobs:ancient_callings`), the book the Arch-Illager drops, drawn as an original black, gold and sculk-teal book.

### Changed

- `mobs` pack: the Arch-Illager is redesigned. It keeps the vanilla illager face and now has a pillager's build in dark slate, a black poncho with gold stripes, a gold pauldron on each shoulder, a crossbow in each hand, a pouch at its hip and a netherite sword on its back. Its six body models and its texture change, ten models for the crossbows, the pouch and the sword (held and sheathed) are added, and the four staff and orb models are removed. Every other existing model, texture and item is unchanged, and so is the pack icon.

## [0.8.0] - 2026-10-05

Daxton's sixth batch of mobs.

### Added

- `mobs` pack: the Hopping Pig as a BetterModel 3.5.0 display model with the vanilla pig's shape and proportions, and an original stand-in texture in the pig layout, `bettermodel:item/hopping_pig_vanilla_pig`.

### Changed

- `mobs` pack: the items atlas, `assets/minecraft/atlases/items.json`, gains a fourth source, which maps the client's own `minecraft:entity/pig/pig_temperate` texture onto the Hopping Pig's sprite. It only names the vanilla texture; no Mojang pixels ship. Every other existing model, texture and item is unchanged, and so is the pack icon.

## [0.7.0] - 2026-10-04

Daxton's fifth batch of mobs.

### Added

- `mobs` pack: the Arch-Illager boss as a BetterModel 3.5.0 display model, in original art — a small illager in a dark grey hooded robe with purple trim and a gold crown, carrying a staff topped by the glowing Orb of Dominance — and one item, the Orb of Dominance (`mobs:orb_of_dominance`), a single full-bright cube.
- `mobs` pack: the items atlas, `assets/minecraft/atlases/items.json`, which maps the client's own `minecraft:entity/illager/pillager` texture onto three face sprites, `bettermodel:item/{arch_illager,enchanter,summoner}_illager_face`. It only names the vanilla texture; no Mojang pixels ship. Each sprite also ships as an original stand-in PNG, which a client shows if it ignores the atlas.

### Changed

- `mobs` pack: the Summoner and the Enchanter now wear the vanilla illager face. Their head and nose take the face texture at the vanilla illager's UVs, and their drawn eyes and brow are gone. Only `enchanter_h_head_1.json` and `summoner_h_head_1.json` change; every other existing model, texture and item is unchanged, and so is the pack icon.

## [0.6.0] - 2026-10-04

Daxton's fourth batch of mobs.

### Added

- `mobs` pack: two more mobs as BetterModel 3.5.0 display models — the Summoner, and the Enchanter as a 3D model in the style of Minecraft Dungeons, with the enchanting book it carries. Every existing model and item is unchanged.

### Changed

- `mobs` pack: the pack icon is now a front view of the Enchanter model's head and hat, drawn from the pack's own art.

### Removed

- `mobs` pack: the Illusioner recolour (`assets/minecraft/textures/entity/illager/illusioner.png`, the four rules, the `[preview]` and the `[vanilla]` source), replaced by the Enchanter model. The pack is now its files alone and its build downloads nothing. The separate `enchanter` pack is unchanged and keeps the recolour.

## [0.5.0] - 2026-10-03

Daxton's third batch of mobs.

### Added

- `mobs` pack: two more mobs as BetterModel 3.5.0 display models — the Bear and the Piston Golem. Every existing model and item is unchanged.

## [0.4.0] - 2026-10-03

Daxton's second batch of mobs.

### Added

- `mobs` pack: twelve more mobs as BetterModel 3.5.0 display models — the eight soul-corrupted mobs (Soul Zombie, Soul Husk, Soul Drowned, Soul Skeleton, Soul Stray, Soul Creeper, Soul Spider and Soul Zombie Villager), the Sculk Sniffer, the Jellyfish, the Tropical Fish Slime and the Tuff Golem — and one item, the Tropical Slime (`mobs:tropical_slime`). The Enchanter, the four Sift mobs and the three existing items are unchanged.

## [0.3.0] - 2026-10-01

The mobs pack.

### Added

- `mobs` pack for Minecraft Java 26.3 (resource pack format 97): every custom mob look in the one pack a server can send. It repeats the `enchanter` pack's four rules unchanged (a test keeps the two in step) and adds four mobs as BetterModel 3.5.0 display models — the Blob, the Sifter, the Harmonizer and the Twisted Harmonizer — and three items: Jello, the Harmonizer Tentacle and the Cooked Harmonizer Tentacle.

## [0.2.0] - 2026-10-01

Data packs, and the first one.

### Added

- Data packs: `kind = "data"` in a pack's `[pack]` table builds a data pack from `files/` alone. Every file must sit under `files/data/` (`pack.png` aside), every `.json` must parse, and `[vanilla]`, `[[textures]]` and `[preview]` are refused. `kind` defaults to `"resource"`, so existing packs build unchanged, with the same SHA-1. `build` labels a data pack's SHA-1 `DATA_PACK_SHA1=`.
- `sift` data pack for Minecraft Java 26.3 (data pack format 121): one dimension, `sift:the_sift`, in the style of the Sift from *Minecraft Dungeons II* — Singer's Meadow (teal grass, rust-red clearings, blue-leaved acacia and oak, pink-violet sky) and the Carapace (sculk, orange terracotta, deepslate, ochre sky), on vanilla terrain shapes. No client install.

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
