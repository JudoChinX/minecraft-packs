# Pack Definition Reference

Every pack lives in its own directory, `packs/<name>/`, and is defined by a `pack.toml` there. The
directory name is the pack's name and the stem of its zip (`<name>-<version>.zip`), so it may use
only lowercase `a-z`, `0-9`, `-` and `_`.

Unknown keys are rejected, not ignored: a misspelt key fails the build instead of silently producing
a different pack. [`packs/enchanter/pack.toml`](../packs/enchanter/pack.toml) is the worked example.

---

## `[pack]` (required)

Written to the zip's `pack.mcmeta`.

| Key | Type | Meaning |
|---|---|---|
| `description` | string | The text shown in the client's resource pack list. |
| `min_format` | integer | The lowest resource pack format the pack supports. |
| `max_format` | integer | The highest; must be at least `min_format`. |
| `kind` | string | Optional. `"resource"` (the default) or `"data"`. See *Data packs* below. |

Since Minecraft 25w31a, packs declare `min_format`/`max_format` instead of `pack_format`; a pack only
needs `pack_format` as well if it also claims formats below 65. An integer `max_format` covers every
minor version of that major format. A release's format is its client jar's `version.json`
`pack_version` (26.3 is 97.1).

## `[vanilla]` (required when the pack recolours textures)

The Minecraft release whose official client jar the textures are read from.

| Key | Type | Meaning |
|---|---|---|
| `version` | string | The release id in Mojang's version manifest, e.g. `"26.3"`. |
| `client_sha1` | string | The client jar's SHA-1, lowercase hex. It must equal the SHA-1 Mojang's manifest lists, and the downloaded jar must match it. |

Changing `version` means re-checking every texture's `sha256` against a fresh preview.

## `[[textures]]` (optional, repeatable)

One entry per vanilla texture the pack recolours.

| Key | Type | Meaning |
|---|---|---|
| `path` | string | The texture's path inside the client jar and inside the pack, e.g. `"assets/minecraft/textures/entity/illager/illusioner.png"`. Lowercase, under `assets/`, ending `.png`. |
| `sha256` | string | The vanilla texture's SHA-256, lowercase hex. The build refuses a texture that does not match, because a changed vanilla texture means the rules need reviewing. |
| `rules` | array of tables | The recolour rules, in priority order; at least one. |

### `[[textures.rules]]`

Each colour in the texture (each palette entry for a palette image, each opaque pixel otherwise) is
tested against the rules in order, and the **first** rule whose three ranges all contain it wins. A
colour matching no rule is left untouched. Colours are compared in HLS: hue in degrees, saturation
and lightness as fractions from 0 to 1. Every range is inclusive at both ends.

| Key | Type | Meaning |
|---|---|---|
| `name` | string | A label, reported in the build's per-rule counts. |
| `hue` | `[low, high]` | Hue range in degrees, `0 <= low <= high <= 360`. |
| `saturation` | `[low, high]` | Saturation range, `0 <= low <= high <= 1`. |
| `lightness` | `[low, high]` | Lightness range, `0 <= low <= high <= 1`. |
| `target_hue` | number | The hue a matching colour takes, 0-360. |
| `target_saturation` | number | The saturation it takes, 0-1. |
| `lightness_offset` | number | Added to the colour's own lightness, clamped to 0-1. This keeps the texture's shading. |

A palette image keeps its mode, pixel indices and transparency; its transparent palette entry is
never recoloured. A non-palette image is converted to RGBA and keeps each pixel's alpha.

## `[preview]` (optional)

Renders the review sheet (the recoloured texture and a flat front view of the model; the vanilla
texture is never drawn), and generates the pack's `pack.png` icon from the model's face.

| Key | Type | Meaning |
|---|---|---|
| `texture` | string | The `path` of one of the pack's `[[textures]]`. |
| `model` | string | The model layout to draw the front view with. Known layouts: `illager`. |
| `title` | string | The pack's name for the mob, used in the sheet's labels, e.g. `"Enchanter"`. |

A new model layout is a table of box UVs and offsets in `minecraft_packs/models.py`, taken from the
vanilla model class.

## `files/` (optional)

Every file under `packs/<name>/files/` is copied into the zip at the same relative path, for content
that is not a recolour: models, sounds, language files, or a hand-made `pack.png`. Dotfiles are
skipped. A file may not replace one the build generates (`pack.mcmeta`, a recoloured texture, or a
generated `pack.png`); that fails the build.

Never put Mojang's original assets here. Anything derived from them belongs in a rule, built at
build time.

Every pack needs a `pack.png`: either a `[preview]` to generate it, or `files/pack.png`.

## Data packs

A pack with `kind = "data"` is a data pack: worldgen, dimensions, loot tables and the like, which a
server loads from its world's `datapacks/` folder rather than sending to clients. Its content is
`files/` alone:

- every file sits under `files/data/` (plus `files/pack.png`, which is still required);
- every `.json` file must parse, so a stray comma fails the build rather than the server's start;
- `[vanilla]`, `[[textures]]` and `[preview]` are refused, since there is nothing to recolour.

`min_format`/`max_format` are then **data** pack formats, which differ from resource pack formats: a
release's is its server or client jar's `version.json` `pack_version.data_major` (26.3 is 121.0).

A data pack refers to vanilla worldgen by id (`minecraft:overworld/continents`, `minecraft:trees_savanna`)
and copies none of it, apart from small numeric settings that a new registry entry has to restate;
any such copy is named, with its source, in the pack's README.

## `expected.sha1` (recommended)

One line: the lowercase hex SHA-1 the pack's zip is expected to have. `build` compares every zip
with it and warns on a mismatch; `build --check`, which CI and the release job use, fails instead.
After an intended change to a pack, record the new value and commit it:

```bash
python -m minecraft_packs build --update-expected <name>
```

The zip's name carries the release version but its bytes do not, so a pack that did not change keeps
its SHA-1 from release to release.
