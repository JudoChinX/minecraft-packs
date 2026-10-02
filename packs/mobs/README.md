# mobs

Every custom mob look on the server this repository serves, as one resource pack (a server can send only one):

- **The Enchanter** — the [`enchanter`](../enchanter/) pack's recolour of the Illusioner, its four rules repeated
  here unchanged. A test fails if the two packs drift apart.
- **The Sift mobs** — the Blob, the Sifter, the Harmonizer and the Twisted Harmonizer, as
  [BetterModel](https://modrinth.com/plugin/bettermodel) display models under `assets/bettermodel/`. BetterModel
  3.5.0 generated them from Blockbench models that are this project's own work (configuration
  `pack.use-obfuscation: false`, so the paths are the model and bone names). A server that uses them runs
  BetterModel with the same models; regenerate these files whenever a model changes.
- **Three items** under `assets/mobs/`: Jello, the Harmonizer Tentacle and the Cooked Harmonizer Tentacle, for items
  carrying an `item_model` of `mobs:jello`, `mobs:harmonizer_tentacle` or `mobs:cooked_harmonizer_tentacle`.

Every file under `files/` is original art; nothing is taken from Mojang's assets. The zip's expected SHA-1 is in
[`expected.sha1`](expected.sha1).
