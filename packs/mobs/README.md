# mobs

Every custom mob look on the server this repository serves, as one resource pack (a server can send only one):

- **The Enchanter** — the [`enchanter`](../enchanter/) pack's recolour of the Illusioner, its four rules repeated
  here unchanged. A test fails if the two packs drift apart.
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
- **Four items** under `assets/mobs/`: Jello, the Harmonizer Tentacle, the Cooked Harmonizer Tentacle and the Tropical
  Slime, for items carrying an `item_model` of `mobs:jello`, `mobs:harmonizer_tentacle`,
  `mobs:cooked_harmonizer_tentacle` or `mobs:tropical_slime`.

Every file under `files/` is original art; nothing is taken from Mojang's assets. The zip's expected SHA-1 is in
[`expected.sha1`](expected.sha1).
