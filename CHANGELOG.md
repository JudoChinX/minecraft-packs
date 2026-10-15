# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.19.10] - 2026-10-15

minecraft-ref: 9ca9bffb89d9dde203f016c8274d97f924c05c03

### Changed

- New Goblin skin, painted by Daxton.

## [0.19.9] - 2026-10-15

minecraft-ref: 9dc88db1b16fdae2aab877ce0d6b75022471293f

### Changed

- New Archevoker skin, painted by Daxton.

## [0.19.8] - 2026-10-15

minecraft-ref: 72d180a162e412b992548078ad5a62a85028962c

### Changed

- New Enchanter skin, painted by Daxton.

## [0.19.7] - 2026-10-15

minecraft-ref: 24e550b329a10305ceacbba85772ba8906ba122d

### Changed

- New Harmonizer skin, painted by Daxton.

## [0.19.6] - 2026-10-15

minecraft-ref: e571d331fd0704024968467ed06d3c962d340ee2

### Changed

- New Geomancer skin, painted by Daxton.

## [0.19.5] - 2026-10-15

minecraft-ref: 77565ad0d1a29be85e82f7b40a9a1fc75fc6419a

### Changed

- New Iceologer skin, painted by Daxton.

## [0.19.4] - 2026-10-14

minecraft-ref: f5a3d965c8b7f64dc9adb2c9445bd5842939be3c

### Changed

- New Crocofang skin, painted by Daxton.

## [0.19.3] - 2026-10-14

minecraft-ref: ba9c48a73f3a283a2ee18621311385fa6cb270ec

### Changed

- New Miner skin, painted by Daxton.

## [0.19.2] - 2026-10-14

minecraft-ref: a9a3e83b7cdacb9b5d346e621646dbaef1067b2b

### Changed

- New Jellyfish skin, painted by Daxton.

## [0.19.1] - 2026-10-14

minecraft-ref: a78af36824b322da748424c3e72a1c9b1ec43cba

### Changed

- Releases carry a fixed-name `mobs.zip` asset and are published not-latest.
- New Magger skin, painted by Daxton.

## [0.19.0] - 2026-10-13

The mobs pack's seventeenth batch: Daxton's Redstone Golem, Charged Redstone Golem and Archevoker, redrawn after his pictures.

### Added

- `mobs` pack: stone skin textures (original) for the three redrawn mobs, one texel a pixel on 64 x 64 sheets: `bettermodel:item/redstone_golem_stone_1` to `_5`, `bettermodel:item/charged_redstone_golem_stone_1` to `_5` and `bettermodel:item/archevoker_stone_1`; and the Charged Redstone Golem's glow textures, `bettermodel:item/charged_redstone_golem_glow_1` to `_4`, which carry its lit cracks and nothing else.

### Changed

- `mobs` pack: the Redstone Golem and the Charged Redstone Golem are redrawn as stone bricks and cobbles with branching cracks (dark red with patches of redstone; on the charged one orange to yellow and lit), with a bigger head and shoulders; the Archevoker's robe opens down the front (gold trim, an orange lining, near-black between) and its head, shoulder pads, hands and legs are speckled stone. Their display models and palette textures change; the Archevoker's face is still the client's pillager face by the atlas, so no Mojang pixels ship. Every other existing model, texture and item is unchanged, and so is the pack icon.

## [0.18.0] - 2026-10-12

The mobs pack's sixteenth batch: Daxton's Wicked Geomancer and its necklace.

### Added

- `mobs` pack: one more mob as a BetterModel 3.5.0 display model — the Wicked Geomancer, with its stand-in illager face texture (original), `bettermodel:item/wicked_geomancer_illager_face`, for the atlas to replace — and one item, the Wicked Geomancer's Necklace (`mobs:wicked_geomancers_necklace`, an original 16 px texture).

### Changed

- `mobs` pack: the items atlas, `assets/minecraft/atlases/items.json`, routes the client's pillager face to the Wicked Geomancer too (one `minecraft:single` source more). It only names the vanilla textures; no Mojang pixels ship. Every other existing model, texture and item is unchanged, and so is the pack icon.

## [0.17.0] - 2026-10-12

The mobs pack's fifteenth batch: Daxton's Iceologer, Wielder, Magger and Wicked Magger.

### Added

- `mobs` pack: four more mobs as BetterModel 3.5.0 display models — the Iceologer and the Wielder, each with its stand-in illager face texture (original), `bettermodel:item/iceologer_illager_face` and `bettermodel:item/wielder_illager_face`, for the atlas to replace; and the Magger and the Wicked Magger (one geometry, two palettes, all original).

### Changed

- `mobs` pack: the items atlas, `assets/minecraft/atlases/items.json`, routes the client's pillager face to the Iceologer and the Wielder too (two `minecraft:single` sources more). It only names the vanilla textures; no Mojang pixels ship. Every other existing model, texture and item is unchanged, and so is the pack icon.

## [0.16.0] - 2026-10-12

The mobs pack's fourteenth batch: Daxton's Miner and Archevoker.

### Added

- `mobs` pack: two more mobs as BetterModel 3.5.0 display models — the Archevoker and the Miner, each with its stand-in illager face texture (original), `bettermodel:item/archevoker_illager_face` and `bettermodel:item/miner_illager_face`, for the atlas to replace.

### Changed

- `mobs` pack: the items atlas, `assets/minecraft/atlases/items.json`, routes the client's pillager face to the Archevoker and the Miner too (two `minecraft:single` sources more). It only names the vanilla textures; no Mojang pixels ship. Every other existing model, texture and item is unchanged, and so is the pack icon.

## [0.15.0] - 2026-10-11

The mobs pack's thirteenth batch: Daxton's Redstone Golem, normal and charged, and the Redstone Golem Head.

### Added

- `mobs` pack: two more mobs as BetterModel 3.5.0 display models — the Charged Redstone Golem and the Redstone Golem; and one item, the Redstone Golem Head (`mobs:redstone_golem_head`), with a second model for the placed head's glowing eyes (`mobs:redstone_golem_head_glow`). Every other existing model, texture and item is unchanged, and so is the pack icon.

## [0.14.0] - 2026-10-11

The mobs pack's twelfth batch: Daxton's Goblin and the coconut, the Crocofang restyled on four legs and a shark-tooth Crocofang Tooth.

### Added

- `mobs` pack: the Goblin as a BetterModel 3.5.0 display model; and one item, the Coconut (`mobs:coconut`).

### Changed

- `mobs` pack: the Crocofang is redrawn on four legs, in ravager greys with a saddle: its eight models (`crocofang_arm_l_1.json`, `crocofang_arm_r_1.json`, `crocofang_h_head_1.json`, `crocofang_jaw_1.json`, `crocofang_leg_l_1.json`, `crocofang_leg_r_1.json`, `crocofang_tail_1.json`, `crocofang_torso_1.json`) and its texture (`crocofang_crocofang.png`) change; its bones keep their names, so its item definitions do not. The Crocofang Tooth (`mobs:crocofang_tooth`) is redrawn as a pale shark tooth (`crocofang_tooth.png`). Every other existing model, texture and item is unchanged, and so is the pack icon.

## [0.13.0] - 2026-10-07

The mobs pack's eleventh batch: Daxton's Oasis blocks, the Palm Log, the Palm Planks, the Palm Slab and Fertilized Sand.

### Added

- `mobs` pack: four blocks, the Fertilized Sand (`mobs:fertilized_sand`), the Palm Log (`mobs:palm_log`, ringed bark and ends on a `cube_column`), the Palm Planks (`mobs:palm_planks`) and the Palm Slab (`mobs:palm_slab`), with their textures, block models and items.
- `mobs` pack: `assets/minecraft/blockstates/brown_mushroom_block.json` and `red_mushroom_block.json`, vanilla's multipart for each with its all-faces-off state drawn as the Palm Log and the Fertilized Sand.
- `mobs` pack: `assets/minecraft/blockstates/petrified_oak_slab.json`, every state drawn as the Palm Slab (its halves) or the Palm Planks (its double). Every other existing model, texture and item is unchanged, and so is the pack icon.

## [0.12.0] - 2026-10-06

The mobs pack's tenth batch: Daxton's Crocofang, the Crocofang Tooth and the throwing knife.

### Added

- `mobs` pack: the Crocofang as a BetterModel 3.5.0 display model; and two items, the Crocofang Tooth (`mobs:crocofang_tooth`) and the Throwing Knife (`mobs:throwing_knife`, a handheld item model). The Damage and Poison Aspect enchantments of the same batch ship inside the server plugin, not in this pack. Every other existing model, texture and item is unchanged, and so is the pack icon.

## [0.11.0] - 2026-10-06

The mobs pack's ninth batch: Daxton's Simphtomer, Geomancer and Infernoillager.

### Added

- `mobs` pack: three more mobs as BetterModel 3.5.0 display models — the Geomancer, the Infernoillager and the Simphtomer, and original stand-in textures for the atlas to replace, `bettermodel:item/geomancer_illager_face`, `bettermodel:item/infernoillager_illager_face` and `bettermodel:item/simphtomer_illager_face`.

### Changed

- `mobs` pack: the items atlas, `assets/minecraft/atlases/items.json`, adds `minecraft:entity/illager/pillager` for the Geomancer, the Infernoillager and the Simphtomer. It only names the vanilla textures; no Mojang pixels ship. Every other existing model, texture and item is unchanged, and so is the pack icon.

## [0.10.0] - 2026-10-06

The mobs pack's eighth batch: Daxton's five pirates, the Pirate Captain, the cutlass, the peg leg and moldy oak planks.

### Added

- `mobs` pack: six more mobs as BetterModel 3.5.0 display models — the five pirates (Scar and Hook, Left Eyepatch, Right Eyepatch, Hook and Pouch, and the Pirate Archer) and the Pirate Captain, and original stand-in textures for the atlas to replace, `bettermodel:item/pirate_1_illager_face`, `bettermodel:item/pirate_2_illager_face`, `bettermodel:item/pirate_3_illager_face`, `bettermodel:item/pirate_4_illager_face`, `bettermodel:item/pirate_5_illager_face` and `bettermodel:item/pirate_captain_illager_face`; and three items, the Cutlass (`mobs:cutlass`), the Moldy Oak Planks (`mobs:moldy_oak_planks`) and the Peg Leg (`mobs:peg_leg`).
- `mobs` pack: `assets/minecraft/blockstates/mushroom_stem.json`, vanilla's multipart for the mushroom stem with the all-faces-off state drawn as the Moldy Oak Planks (`mobs:block/moldy_oak_planks`); every other state names vanilla's own `mushroom_stem` and `mushroom_block_inside` models, unchanged.

### Changed

- `mobs` pack: the items atlas, `assets/minecraft/atlases/items.json`, adds `minecraft:entity/illager/pillager` for the five pirates (Scar and Hook, Left Eyepatch, Right Eyepatch, Hook and Pouch, and the Pirate Archer) and the Pirate Captain. It only names the vanilla textures; no Mojang pixels ship. Every other existing model, texture and item is unchanged, and so is the pack icon.

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
