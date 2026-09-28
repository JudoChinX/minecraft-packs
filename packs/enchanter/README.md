# enchanter

Retextures the vanilla **Illusioner** as a purple-robed, gold-trimmed **Enchanter** in the style of
Minecraft Dungeons.

![The Enchanter: recoloured texture and front view](../../docs/enchanter-preview.png)

The definition is [`pack.toml`](pack.toml): four hue-range rules over the vanilla texture's palette.
The zip's expected SHA-1 is committed in [`expected.sha1`](expected.sha1); CI fails any build that
differs from it.

| Rule | Matches | Becomes |
|---|---|---|
| `robe` | Saturated blue (robe, hood, sleeves) | Deep violet-purple |
| `trim` | Pale blue speckles | Gold trim |
| `amber` | Teal speckles | Darker amber gold |
| `pale` | Blue-violet speckles, which would vanish on purple | Pale gold |

Anything else is untouched, which keeps the grey illager skin, the eyes and the dark shirt.

## Vanilla Source

The texture is read from Mojang's official client jar at build time and is not in this repository.

| | |
|---|---|
| Minecraft version | Java Edition **26.3** (resource pack format 97.1) |
| File | `assets/minecraft/textures/entity/illager/illusioner.png` |
| Obtained from | the official client jar, via Mojang's version manifest |
| Manifest | `https://piston-meta.mojang.com/mc/game/version_manifest_v2.json` |
| Client jar SHA-1 | `e877b6a07acd633fb3bb475002175cec036e7b87` |
| Texture SHA-256 | `f43b9eecec0f7c846f673297c5ceff16b091359c589b8646abf82c5308bbfa75` |
| Texture format | 64 x 64, 8-bit palette (35 colours, index 0 transparent), 1,019 bytes |

If Mojang changes the texture, the build stops at the SHA-256 check. Regenerate the preview, review
the rules against it, and only then update the pin.
