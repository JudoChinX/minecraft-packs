# mobs

Every custom mob look on the server this repository serves, as one resource pack (a server can send only one):

- **The Sift mobs** — the Blob, the Sifter, the Harmonizer and the Twisted Harmonizer, as
  [BetterModel](https://modrinth.com/plugin/bettermodel) display models under `assets/bettermodel/`. BetterModel
  3.5.0 generated them from Blockbench models that are this project's own work (configuration
  `pack.use-obfuscation: false`, so the paths are the model and bone names). A server that uses them runs
  BetterModel with the same models; regenerate these files whenever a model changes.
- **Daxton's second batch**, as BetterModel display models from the same pipeline: the eight soul-corrupted mobs
  (Soul Zombie, Soul Husk, Soul Drowned, Soul Skeleton, Soul Stray, Soul Creeper, Soul Spider and Soul Zombie
  Villager — glowing, translucent light-blue models), the Sculk Sniffer, the Jellyfish, the Tropical Fish Slime and
  the Tuff Golem.
- **Daxton's third batch**, from the same pipeline: the Bear and the Piston Golem.
- **Daxton's fourth batch**, from the same pipeline: the Summoner, an illager in tattered brown robes and a grey cape,
  and the Enchanter as a 3D model in the style of Minecraft Dungeons, with the enchanting book it carries. Their
  animations (the Enchanter's cast among them) are played by BetterModel on the server; the pack holds the models.
- **Daxton's fifth batch**, from the same pipeline: the Arch-Illager, the final boss of Minecraft Dungeons, as original
  art — a small illager in a dark grey hooded robe with purple trim and a gold crown, carrying a staff topped by the
  glowing Orb of Dominance — and the illager face (below) on the Summoner and the Enchanter. Their bodies, robes, hats
  and capes are unchanged. The seventh batch redesigned the Arch-Illager.
- **Daxton's sixth batch**, from the same pipeline: the Hopping Pig, a model with the vanilla pig's shape and
  proportions that wears the client's own pig texture (below). Its hops and backflips are played by the server.
- **Daxton's seventh batch**, from the same pipeline: the Arch-Illager redesigned. It keeps the illager face (below)
  and gains a pillager's build in dark slate, a black poncho with gold stripes, a gold pauldron on each shoulder, a
  crossbow in each hand, a pouch at its hip and a netherite sword on its back; the hood, crown, robe, staff and orb are
  gone. Which weapons show at a time is the server's. The batch also adds the Ancient Callings, the book it drops.
- **Daxton's eighth batch**, from the same pipeline: the five pirates (Scar and Hook, Left Eyepatch, Right Eyepatch,
  Hook and Pouch, and the Pirate Archer) and the Pirate Captain, each wearing the illager face (below), with the
  Cutlass, the Peg Leg and the Moldy Oak Planks.
- **Daxton's ninth batch**, from the same pipeline: the Geomancer, the Infernoillager and the Simphtomer, each wearing
  the illager face (below).
- **Daxton's tenth batch**, from the same pipeline: the Crocofang (original art, no atlas route), the Crocofang Tooth
  and the Throwing Knife.
- **Eleven items** under `assets/mobs/`: Jello, the Harmonizer Tentacle, the Cooked Harmonizer Tentacle, the Tropical
  Slime, the Orb of Dominance, the Ancient Callings, the Cutlass, the Peg Leg, the Crocofang Tooth, the Throwing Knife
  and the Moldy Oak Planks, for items carrying an `item_model` of `mobs:jello`, `mobs:harmonizer_tentacle`,
  `mobs:cooked_harmonizer_tentacle`, `mobs:tropical_slime`, `mobs:orb_of_dominance`, `mobs:ancient_callings`,
  `mobs:cutlass`, `mobs:peg_leg`, `mobs:crocofang_tooth`, `mobs:throwing_knife` or `mobs:moldy_oak_planks`. The Orb of Dominance, the Arch-Illager's trophy, is one cube that glows at full brightness
  (`light_emission` 15). The Ancient Callings is a black, gold and sculk-teal book, original art. The Cutlass and the
  Throwing Knife are handheld models. The Moldy Oak Planks is a block model (`mobs:block/moldy_oak_planks`, a `cube_all`), and the
  placed block is drawn through `assets/minecraft/blockstates/mushroom_stem.json` (below).

Since 0.6.0 the Enchanter is the 3D model, and the pack no longer recolours the Illusioner: it holds no
`assets/minecraft/` texture, and its build downloads nothing from Mojang. Its files under `assets/minecraft/` are the
items atlas below and, since 0.10.0, the mushroom stem's blockstate (below), both JSON files. The recolour lives on, unchanged, in the separate [`enchanter`](../enchanter/) pack. The
pack's icon, `files/pack.png`, is a front view of the Enchanter model's head and hat, drawn from that model and its
texture.

## The illager faces

The Summoner, the Enchanter, the Arch-Illager, the five pirates, the Pirate Captain, the Geomancer, the Infernoillager
and the Simphtomer wear the vanilla illager face, the one the pillager, the vindicator
and the evoker share, without the pack carrying it. Their head and nose use a second texture,
`bettermodel:item/<model>_illager_face`, laid out like the vanilla illager texture. The pack ships that texture as an
original stand-in, `assets/bettermodel/textures/item/<model>_illager_face.png`: a grey-green illager-style face drawn
procedurally by this project's model script. It also ships the items atlas, `assets/minecraft/atlases/items.json`,
with one `minecraft:single` source per face that puts the client's own `minecraft:entity/illager/pillager` texture into
the items atlas under that sprite name. The client merges atlas files from every pack, vanilla first and the server
pack last, and a later source replaces an earlier one with the same sprite name. So the client draws its own pillager
face over the stand-in. A client that ignores the atlas file, or BetterModel's own `build.zip` served without it,
shows the stand-in face, not the missing texture.

## The Hopping Pig's texture

The Hopping Pig uses the same route for its whole body. Its cubes sit on `bettermodel:item/hopping_pig_vanilla_pig`,
at the vanilla pig's UVs, and the pack ships that texture as an original stand-in,
`assets/bettermodel/textures/item/hopping_pig_vanilla_pig.png`: a pink pig drawn procedurally by this project's model
script. A fourth source in the items atlas puts the client's own `minecraft:entity/pig/pig_temperate` texture under that
sprite name, so the client draws its own temperate pig. Without the atlas file it shows the stand-in pig.

## The moldy oak planks' blockstate

The Moldy Oak Planks borrow a block state the game never generates on its own: a mushroom stem with all six faces
`false`. `assets/minecraft/blockstates/mushroom_stem.json` is vanilla's multipart for the stem, whose parts name only
vanilla's own `minecraft:block/mushroom_stem` and `minecraft:block/mushroom_block_inside` models, with one more part
that draws `mobs:block/moldy_oak_planks` when every face is `false`. Every other state looks exactly as in vanilla.
Without the pack, the planks show the mushroom-inside texture on every face.

## Licensing

Every file under `files/` is original art; nothing is taken from Mojang's assets. The illager-face PNGs and the
Hopping Pig's texture are original stand-ins, not copies of Mojang's textures. The items atlas only *references* the
client's own `minecraft:entity/illager/pillager` and `minecraft:entity/pig/pig_temperate` textures by name, and the
mushroom stem's blockstate only *names* the client's own `minecraft:block/mushroom_stem` and
`minecraft:block/mushroom_block_inside` models; the client reads them from its own assets at runtime; no Mojang pixels are shipped in the repository or the zip. The zip's expected SHA-1 is in [`expected.sha1`](expected.sha1).
