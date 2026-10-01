# Roadmap

This document reflects the current direction of Minecraft Packs. No dates are attached — items move when they're ready.

## Planned

- **BetterModel model packs:** custom mob models for the server's plugins, built with [BetterModel](https://github.com/toxicity188/BetterModel). A model pack is mostly original content rather than a recolour, so it will ship its files through a pack's `files/` directory and use the same deterministic zip, SHA-1 and release pipeline.
- **More model layouts:** front-view layouts beyond the illager, so previews and generated icons work for other mobs.
- **Merged server pack:** one zip combining several packs, since a server sends only one.

## Completed

- **Data packs:** `kind = "data"`, and the `sift` dimension pack.
- **`enchanter` pack:** the Illusioner recoloured as a Minecraft Dungeons-style Enchanter.
- **Reproducible builds:** deterministic zips, checked in CI by building twice.
- **Release assets:** each pack's zip and `.sha1` attached to its GitHub Release.

## Out of Scope

- Committing or redistributing Mojang's original assets, or the client jar.
- Telemetry, analytics, or any connection beyond Mojang's download servers.
- Bedrock Edition packs.
- A graphical editor. Packs are rules in `pack.toml`, reviewed through previews.
