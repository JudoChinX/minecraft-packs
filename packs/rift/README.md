# `rift`

A data pack that adds one dimension, **`paradox:rift`**: the Paradox Rift, designed by Daxton. It
needs no client install. The server sends biome colours to every client, and the terrain is built
from vanilla blocks.

| Biome | Ground | Plants and features | Sky, fog, water | Where |
|---|---|---|---|---|
| `paradox:the_rift` ("The Paradox Rift") | grass tinted red (`#b8323c`), patches of moss block (about 15 %, from the surface noise) | sparse oak and dark oak with light-cyan leaves (`#7fe6e6`), red short grass; fire-mud puddles (about 1 chunk in 2) and warped clumps (about 1 in 3) | dusky magenta sky (`#5a1f45`), red fog (`#9a3a4a`), cyan water (`#3fd0d0`), crimson spores | the surface, down to about y -37 |
| `paradox:primary_cave` | deepslate, with blobs of tuff and smooth basalt | none | dark teal fog (`#0f2a2e`), warped spores | `depth` 0.8 and more: everything from about y -37 down to the floor |

- **The dimension type** reaches from **y -416 to 320** (`min_y` -416, `height` 736, `logical_height`
  736). It is the overworld's in everything else: skylight, day and night, beds work, respawn anchors
  do not (`minecraft:gameplay/respawn_anchor_works` false, as the overworld), raids cannot start, and a
  Nether portal spawns no piglins.
- **Terrain shape is vanilla's.** `noise_settings/rift.json` is the vanilla overworld's noise settings
  with only `noise.min_y` and `noise.height` widened to match the dimension type and `material_rule`
  changed to `paradox:rift`. A dimension must have its own noise settings to use its own surface rule
  and height. Those noise settings are numbers and references to vanilla density functions, taken from
  the 26.3 generated data published by
  [misode/mcmeta](https://github.com/misode/mcmeta/tree/26.3-data-json). No other vanilla file is copied.
  Everything else (the dimension, its type, the biomes, the surface rule, the features and the loot
  table) is original, and refers to vanilla features, density functions and surface pieces by id.
- **Below y -64 the stone is solid.** Vanilla's density functions keep their y gradients absolute, so
  the extra 352 blocks have no noise caves, and neither biome lists a carver (vanilla's cave carver
  would reach down to the floor and fill it with lava).
- **Fire mud** (`paradox:fire_mud`): a disk of mud, radius 2-4, in the surface, with a magma-block core
  (radius 0-1) set into its middle, flush with the mud's top and one block deeper. It burns feet that
  do not sneak.
- **Vanilla ores keep their overworld heights** (diamonds from y 16 down, and so on): vanilla placed
  features measured from the world's bottom (`above_bottom`) would sink 352 blocks to the Rift's -416
  floor, so the pack lists `paradox:` copies of the nine that are (`ore_diamond`, `ore_redstone`,
  `ore_lapis_buried` and the rest), on vanilla's configured features, each anchor made the absolute y
  it has in the overworld (bottom -64). The overworld cuts a range off at -64 and the Rift does not, so
  the diamond and lower-redstone ranges reach their full depth (to y -144 and -96).
- **Warped clumps** (`paradox:warped_clump`): a patch of warped wart block with warped nylium cells.
  Warped roots and nether sprouts grow on the nylium only, since they cannot survive on wart.
- **The four Rift ores** are `minecraft:ore` features that place mushroom-block states no vanilla
  placement or feature makes once the server's mushroom-block updates are off (Paper's
  `block-updates.disable-mushroom-block-updates`). The Mobs plugin draws them, and mines and drops them.
  The states, in order, are in [`ORE_STATES`](ORE_STATES), one a line.

| Ore | Feature | Height | Vein size, per chunk | Biomes |
|---|---|---|---|---|
| eatherite | `paradox:eatherite_ore` | y -64 to 100 | 6, ×6 | both |
| pirelite | `paradox:pirelite_ore`, and `paradox:pirelite_ore_lava` (6 more tries a chunk, kept only within 2 blocks of lava or magma) | y -100 to 0 | 4, ×3 | both |
| paralite | `paradox:paralite_ore` | y -200 to -40 | 3, ×2 | both |
| abyslite | `paradox:abyslite_ore`, hidden: a vein block next to air is discarded, as ancient debris | y -400 to -120 | 2, ×1 | the Primary Cave only |

- **`paradox:chests/ancient_ruin`** is the loot table of the chests in the Rift's ancient ruins (placed
  by the Mobs plugin). It draws vanilla's ancient-city chest table once; the plugin adds the Rift's own
  items to it as the chest is opened.
- **Mob spawns** are the vanilla plains' on the surface. The Primary Cave has vanilla's cave monsters
  and bats, but fewer monsters: each has a `spawn_costs` entry (charge 0.7, energy budget 0.15, the
  soul sand valley's), so a monster does not spawn where the monsters already near it would push the
  spot's charge over that budget. Their weights are vanilla's halved, which keeps the mix: weights are
  relative, so halving them alone would not spawn one monster fewer.

## Installing

Put the zip in the primary world's `datapacks/` folder and restart (a `/reload` does not reload
worldgen). Paper creates the world, and Multiverse-Core 5 imports it as `world_paradox_rift`.

**Once the world has generated, never remove the pack.** Its chunks name `paradox:` biomes and hold
the ore states. Delete the world first, then the pack. A new version of the pack changes only chunks
generated after it.
