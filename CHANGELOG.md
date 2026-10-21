# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.27.5] - 2026-10-21

minecraft-ref: ddddf6adb99dcda05b5612155d7cb27020ae52ee

### Changed

- New Harmonizer skin, painted by Daxton.

## [0.27.4] - 2026-10-21

minecraft-ref: 54e1864c18dde6e96ee05f8d4e77138994b32490

### Changed

- New Scorched skin, painted by Daxton.

## [0.27.3] - 2026-10-21

minecraft-ref: d02e41c83db8157c637a1248de3b41799a0895be

### Changed

- New Burned skin, painted by Daxton.

## [0.27.2] - 2026-10-21

minecraft-ref: b88d6103184e518abed20ae0e5ef6ec4a36a479e

### Changed

- New Crystallized skin, painted by Daxton.

## [0.27.1] - 2026-10-21

minecraft-ref: 8cb30b76b8f3295cb528c57e8d6a105a006b2aec

### Changed

- New Frilled Anemone skin, painted by Daxton.

## [0.27.0] - 2026-10-21

The mobs pack's twenty-sixth batch: Daxton's Invader redrawn after his picture.

### Changed

- `mobs` pack: the Invader is redrawn after Daxton's picture: a closed navy helm with a gold band, gold corner caps, a grey T nose guard and a neck flap; red sleeves under grey pauldrons; a red cape with gold edges; a big gold-framed shield of red rings held in front; a long glowing teal blade. These files change: `invader_arm_l_1.json`, `invader_arm_r_1.json`, `invader_h_head_1.json`, `invader_leg_l_1.json`, `invader_leg_r_1.json`, `invader_mantle_1.json`, `invader_shield_1.json`, `invader_spear_1.json`, `invader_torso_1.json` and `invader_invader.png` change. Every other existing model, texture and item is unchanged, and so is the pack icon.

### Security

- Pillow 12.3.0 → 13.0.0 (CVE-2026-112395, -112397, -112400, -112404, -112895, -112896, -112897, -112899, found by
  `pip-audit`); every pack builds byte-identical under it.

## [0.26.4] - 2026-10-19

minecraft-ref: abe176a7fde957e6d24f3c4e47927e0344fcc3c5

### Changed

- New Echo Shard Golem skin, painted by Daxton.

## [0.26.3] - 2026-10-19

minecraft-ref: 05092091ecddbf9517aa03f9f5912654c62e0225

### Changed

- New Crab Blue skin, painted by Daxton.

## [0.26.2] - 2026-10-19

minecraft-ref: cb315f4f3d559df3d801365373fdb8d3b98413e3

### Changed

- New Illadator skin, painted by Daxton.

## [0.26.1] - 2026-10-19

minecraft-ref: c19be6ee1641031654d4363d9464063dbc912738

### Changed

- New Burned skin, painted by Daxton.

## [0.26.0] - 2026-10-19

The mobs pack's twenty-fifth batch: Daxton's Sea Urchin, Urchin Spikes and the Spike Trap (a borrowed tripwire state, open and shut).

### Added

- `mobs` pack: the Sea Urchin as a BetterModel 3.5.0 display model; and two items, the Spike Trap (`mobs:spike_trap`) and the Urchin Spikes (`mobs:urchin_spikes`).
- `mobs` pack: the Spike Trap's block models, `assets/mobs/models/block/spike_trap.json` (open) and `spike_trap_shut.json`, and its block texture, `assets/mobs/textures/block/spike_trap.png`.
- `mobs` pack: the tripwire's blockstate, `assets/minecraft/blockstates/tripwire.json`: the client's own 32 tripwire variants, each narrowed to `disarmed=false` and naming only vanilla's tripwire models, plus the 32 `disarmed=true` variants drawn as the Spike Trap, open or shut. A disarmed tripwire never rests in a survival world, so every tripwire a player or a structure makes draws exactly as before. It only names models; no Mojang pixels ship. Every other existing model, texture and item is unchanged, and so is the pack icon.

## [0.25.0] - 2026-10-18

The mobs pack's 23rd and 24th batches: the Mallard Duck, the Crab (blue, green and red), the Scorched, the Illadator and the Sword Illadator.

### Added

- `mobs` pack: seven more mobs as BetterModel 3.5.0 display models — the Mallard Duck, the Crab (blue, green and red), the Scorched, the Illadator and the Sword Illadator, and original stand-in textures for the atlas to replace, `bettermodel:item/illadator_illager_face` and `bettermodel:item/illadator_sword_illager_face`; and three items, the Ancient Staff (`mobs:ancient_staff`), the Crab Claw (`mobs:crab_claw`) and the Illadator Crown (`mobs:illadator_crown`).
- `mobs` pack: `assets/mobs/equipment/illadator_crown.json`.
- `mobs` pack: `assets/mobs/textures/entity/equipment/humanoid/illadator_crown.png`.

### Changed

- `mobs` pack: the items atlas, `assets/minecraft/atlases/items.json`, adds `minecraft:entity/illager/pillager` for the Illadator and the Sword Illadator. It only names the vanilla textures; no Mojang pixels ship. Every other existing model, texture and item is unchanged, and so is the pack icon.

## [0.24.0] - 2026-10-17

The mobs pack's 21st batch (look only): the Magger's and the Wicked Magger's capes sway behind them.

### Changed

- `mobs` pack: the Magger's and the Wicked Magger's capes hang behind the skirt and legs instead of inside them (`magger_mantle_1.json`, `wicked_magger_mantle_1.json`). Every other existing model, texture and item is unchanged, and so is the pack icon.

## [0.23.0] - 2026-10-16

The mobs pack's 22nd batch: the Crystallized, the Burned, the Anemone (pink, blue, yellow and red) and the Frilled Anemone.

### Added

- `mobs` pack: seven more mobs as BetterModel 3.5.0 display models — the Crystallized, the Burned, the Anemone (pink, blue, yellow and red) and the Frilled Anemone; and four items, the Anemone Membrane (`mobs:anemone_membrane`), the Cooked Anemone Membrane (`mobs:cooked_anemone_membrane`), the Geode (`mobs:geode`) and the Geode Spear (`mobs:geode_spear`). Every other existing model, texture and item is unchanged, and so is the pack icon.

## [0.22.0] - 2026-10-16

The mobs pack's twentieth batch: Daxton's Redstone Golems rebuilt after his picture, and his Wielder's wand, hair and cape.

### Changed

- `mobs` pack: the Redstone Golem and the Charged Redstone Golem redrawn: an upright block, a big head set into its top front, straight arms from shoulder blocks with two long fingers, short square legs, and large cobbles with red patches on the shoulders and veins elsewhere (the charged one's lit). The Wielder redrawn: a wand held out in its hand, tall ragged hair and a red-orange cape on a strap, on skins of its own (`wielder_robe_1-3.png`). The Redstone Golem Head's two textures (`mobs:redstone_golem_head`, `mobs:redstone_golem_head_glow`) redrawn to match. No mob or item is added or removed; as files only, `wielder_wielder.png` (unused), `redstone_golem_stone_6.png`, `charged_redstone_golem_stone_6.png` and `charged_redstone_golem_glow_5.png`/`_glow_6.png` are removed. Every other existing model, texture and item is unchanged, and so is the pack icon.

## [0.21.0] - 2026-10-16

The mobs pack's nineteenth batch: the Echo Shard Golem, the Invader, the Lapis Golem and the Monkey.

### Added

- `mobs` pack: four more mobs as BetterModel 3.5.0 display models — the Echo Shard Golem, the Invader, the Lapis Golem and the Monkey, and an original stand-in texture for the atlas to replace, `bettermodel:item/invader_illager_face`; and two items, the Banana (`mobs:banana`) and the Illager Crown (`mobs:illager_crown`).
- `mobs` pack: `assets/mobs/equipment/illager_crown.json`.
- `mobs` pack: `assets/mobs/textures/entity/equipment/humanoid/illager_crown.png`.

### Changed

- `mobs` pack: the items atlas, `assets/minecraft/atlases/items.json`, adds `minecraft:entity/illager/pillager` for the Invader. It only names the vanilla textures; no Mojang pixels ship. Every other existing model, texture and item is unchanged, and so is the pack icon.
- Tests: the pack test resolves an equipment asset's layer textures (`textures/entity/equipment/<layer>/<name>.png`).

## [0.20.5] - 2026-10-15

minecraft-ref: c621e6c6a339068fcaad592dc1412bc21651c70e

### Changed

- New Tuff Golem skin, painted by Daxton.

## [0.20.4] - 2026-10-15

minecraft-ref: 2b2d56d38b7fb6d29ffbac147b75f2ce05f5715a

### Changed

- New Piston Golem skin, painted by Daxton.

## [0.20.3] - 2026-10-15

minecraft-ref: 7613f27d17f2206ffe75bda3fe39dfa718a832de

### Changed

- New Twisted Harmonizer skin, painted by Daxton.

## [0.20.2] - 2026-10-15

minecraft-ref: 2deac24ff690c2a895072e906a03e63bf325ed9e

### Changed

- New Infernoillager skin, painted by Daxton.

## [0.20.1] - 2026-10-15

minecraft-ref: 6347a3d3e9cf732da435026f00f10f3b1964b5e1

### Changed

- New Pirate 1 skin, painted by Daxton.

## [0.20.0] - 2026-10-15

The mobs pack's eighteenth batch: Daxton's Redstone Golems reshaped and his Wicked Geomancer glowing.

### Changed

- `mobs` pack: the Redstone Golem Head (`mobs:redstone_golem_head`), the Redstone Golem Head Glow (`mobs:redstone_golem_head_glow`), the Wicked Geomancer's Necklace (`mobs:wicked_geomancers_necklace`), the Charged Redstone Golem, the Redstone Golem and the Wicked Geomancer change: `redstone_golem_head.png`, `redstone_golem_head_glow.png`, `wicked_geomancers_necklace.png`, `charged_redstone_golem_arm_l_1.json`, `charged_redstone_golem_arm_r_1.json`, `charged_redstone_golem_h_head_1.json`, `charged_redstone_golem_leg_l_1.json`, `charged_redstone_golem_leg_r_1.json`, `charged_redstone_golem_torso_1.json`, `charged_redstone_golem_charged_redstone_golem.png`, `charged_redstone_golem_glow_1.png`, `charged_redstone_golem_glow_2.png`, `charged_redstone_golem_glow_3.png`, `charged_redstone_golem_glow_4.png`, `charged_redstone_golem_stone_1.png`, `charged_redstone_golem_stone_2.png`, `charged_redstone_golem_stone_3.png`, `charged_redstone_golem_stone_4.png`, `charged_redstone_golem_stone_5.png`, `redstone_golem_arm_l_1.json`, `redstone_golem_arm_r_1.json`, `redstone_golem_h_head_1.json`, `redstone_golem_leg_l_1.json`, `redstone_golem_leg_r_1.json`, `redstone_golem_torso_1.json`, `redstone_golem_redstone_golem.png`, `redstone_golem_stone_1.png`, `redstone_golem_stone_2.png`, `redstone_golem_stone_3.png`, `redstone_golem_stone_4.png`, `redstone_golem_stone_5.png`, `wicked_geomancer_arm_l_1.json`, `wicked_geomancer_arm_r_1.json`, `wicked_geomancer_h_head_1.json`, `wicked_geomancer_leg_l_1.json`, `wicked_geomancer_leg_r_1.json`, `wicked_geomancer_staff_1.json` and `wicked_geomancer_torso_1.json` change, `charged_redstone_golem_glow_5.png`, `charged_redstone_golem_glow_6.png`, `charged_redstone_golem_stone_6.png`, `redstone_golem_stone_6.png`, `wicked_geomancer_glow_1.png`, `wicked_geomancer_robe_1.png` and `wicked_geomancer_robe_2.png` are added, and `wicked_geomancer_wicked_geomancer.png` is removed. Every other existing model, texture and item is unchanged, and so is the pack icon.

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
