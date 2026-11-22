# built-mobs

The mobs that kids build in the Mobs plugin's builder: one `built_<name>.json` (the mob) and, when it has a model,
one `built_<name>.bbmodel` per mob.

Only the `build.yml` and `undo.yml` workflows in `JudoChinX/minecraft` write here; they commit straight to `main` and tag.
Nothing in this directory is edited by hand, except `built_manier.json`, a repo spec copied byte for byte from
`plugins/mobs/built/` in `JudoChinX/minecraft` (it has no `.bbmodel`: its model is a `make_models` model).

Every release zips the `built_*.json` and `built_*.bbmodel` files, sorted and with fixed timestamps, into
`built-mobs.zip` and publishes it with `built-mobs.sha256` (`<sha256>  built-mobs.zip`). This README is not in the zip.
The server's updater downloads both. An empty directory still produces a valid, empty zip.
