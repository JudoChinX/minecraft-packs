# `sift`

A data pack that adds one dimension, **`sift:the_sift`**, in the style of the Sift from
*Minecraft Dungeons II*. It needs no client install. The server sends biome colours to every
client, and the terrain is built from vanilla blocks.

| Biome | Ground | Plants | Sky, fog, water | Where |
|---|---|---|---|---|
| `sift:singers_meadow` | teal-tinted grass with rust-red terracotta clearings, a little sculk; red terracotta beneath | blue-leaved acacia and oak (`trees_savanna`), meadow flowers | pink-violet sky, rose fog, teal water, drifting warped spores | erosion 0 to 1 (smoother land) |
| `sift:carapace` | sculk threaded with orange terracotta, deepslate outcrops; deepslate beneath | sparse grass | ochre sky, rust fog, dark purple water, crimson spores | erosion -1 to 0 (rugged land) |

- **Terrain shape is vanilla's.** `noise_settings/sift.json` is the vanilla overworld's noise settings
  with only `material_rule` changed to `sift:sift`. A dimension must have its own noise settings to use
  its own surface rule. Those noise settings are numbers and references to vanilla density functions,
  taken from the 26.3 generated data published by
  [misode/mcmeta](https://github.com/misode/mcmeta/tree/26.3-data-json). No other vanilla file is copied.
  Everything else (biomes, the surface rule, the dimension) is original, and refers to vanilla
  features, density functions and surface pieces by id.
- **The dimension type is `minecraft:overworld`**: overworld height, day and night, beds work.
- **Mob spawns** are the vanilla meadow's in Singer's Meadow. The Carapace has the same monsters and no animals.

## Installing

Put the zip in the primary world's `datapacks/` folder and restart (a `/reload` does not reload
worldgen). Paper creates the world, and Multiverse-Core 5 imports it as `world_sift_the_sift`.

**Once the world has generated, never remove the pack.** Its chunks name `sift:` biomes. Delete
the world first, then the pack. A new version of the pack changes only chunks generated after it.
