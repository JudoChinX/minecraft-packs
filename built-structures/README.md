# built-structures

The structures that kids build in Minecraft and send from the Mobs plugin's board: one `built_<name>.nbt` (the
structure template) and one `built_<name>.json` (its sidecar) per structure.

Only the `structure.yml` workflow in `JudoChinX/minecraft` writes here, mirroring the minecraft repo's
`plugins/mobs/structures/built/`; it commits straight to `main`. Nothing in this directory is edited by hand.

Every release zips the `built_*.nbt` and `built_*.json` files, sorted and with fixed timestamps, into
`built-structures.zip` and publishes it with `built-structures.sha256` (`<sha256>  built-structures.zip`). This
README is not in the zip. The server's updater downloads both and registers the structures live. An empty
directory still produces a valid, empty zip.
