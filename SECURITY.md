# Security Policy

## What Minecraft Packs Does

Understanding what the software accesses and why is important for trust. There are two parts: the
**build**, which runs on your machine or in CI, and the **packs**, which a Minecraft client downloads
from a server.

The build downloads three things from Mojang, over HTTPS, and nothing else. The packs are data:
images and JSON, with no code.

To be absolutely clear, Minecraft Packs does not and will never:
- Collect usage statistics or telemetry
- Phone home or check for updates
- Contact any host other than Mojang's download servers
- Upload anything anywhere (publishing a release is done by GitHub Actions, from the tagged commit)
- Write anywhere but the output directory (`dist/` by default), the cache (`.cache/` by default), the
  `OUT` path you give `preview`, and — only when you pass `build --update-expected` — each pack's
  `packs/<name>/expected.sha1`
- Need or read any credentials

## Verify It Yourself

The build is a handful of small modules. The links below track the `main` branch:

- [`minecraft_packs/vanilla.py`](https://github.com/JudoChinX/minecraft-packs/blob/main/minecraft_packs/vanilla.py) — every network request the build makes, and every check on what comes back
- [`minecraft_packs/build.py`](https://github.com/JudoChinX/minecraft-packs/blob/main/minecraft_packs/build.py) — how a pack is assembled
- [`minecraft_packs/archive.py`](https://github.com/JudoChinX/minecraft-packs/blob/main/minecraft_packs/archive.py) — the deterministic zip and its verification
- [`minecraft_packs/config.py`](https://github.com/JudoChinX/minecraft-packs/blob/main/minecraft_packs/config.py) — validation of pack definitions

The only runtime dependency is [Pillow](https://github.com/python-pillow/Pillow), pinned to an exact
version, widely used, and with a public security disclosure policy. Everything else is the Python
standard library.

## What the Build Downloads

On a cache miss, and only for packs that recolour vanilla textures:

1. `GET https://piston-meta.mojang.com/mc/game/version_manifest_v2.json` — Mojang's version manifest,
   which lists each release's version JSON and its SHA-1.
2. `GET` the release's version JSON, at the URL the manifest lists. Its SHA-1 must match the manifest.
3. `GET` the release's client jar, at the URL the version JSON lists (on `piston-data.mojang.com`).

The build only starts a download from an `https://` URL; any other scheme in a Mojang response is
refused. It does not pin the transport beyond that: Python's `urllib` follows HTTP redirects, and a
redirect could in principle leave HTTPS. Integrity does not rest on the transport. The manifest is
the one file with no pinned hash — it is only used to find the other two — and everything the build
uses is checked against a hash, so a tampered or redirected response can make a build fail but cannot
change what it produces.

**How what comes back is verified:**
- The client jar's SHA-1 must equal the SHA-1 Mojang's version JSON lists **and** the SHA-1 pinned in
  the pack's `pack.toml`. A mismatch with either fails the build.
- A cached jar is re-hashed on every use and downloaded again if it no longer matches the pin.
- Every texture read out of the jar must match the SHA-256 pinned in `pack.toml`. If Mojang changes a
  texture, the build stops rather than shipping a recolour nobody reviewed.
- Downloads are written to a temporary file and moved into place, so an interrupted download never
  leaves a jar that looks complete.

SHA-1 is used because it is what Mojang publishes for its downloads and what a Minecraft client uses
to check a server resource pack. It is an integrity check against corruption and accidental change.
The pinned SHA-256 of each texture is the stronger guarantee of what a pack is built from.

## What the Packs Contain

A pack zip contains `pack.mcmeta` (JSON), `pack.png`, recoloured PNG textures, and any files a pack
ships verbatim from its `files/` directory. `verify` checks that every PNG decodes and that
`pack.mcmeta` is well formed. A resource pack cannot run code on a Minecraft client.

The client checks a downloaded pack against the SHA-1 the server announces, and rejects it on a
mismatch. Publish the `.sha1` from the same release as the zip.

## CI and Releases

- Every workflow runs with `permissions: {}` at the top level; each job is granted only what it
  needs, and only the release job may write (`contents: write`, to create the release).
- The jobs that build packs install Pillow from `requirements-hashes.txt` with `--require-hashes`, so
  a package that differs from the one reviewed is refused.
- Every build in CI runs with `--check`: a zip whose SHA-1 differs from the pack's committed
  `expected.sha1` fails the job, so a release can only publish the SHA-1s already in the repository.
- Every third-party action is pinned to a full commit SHA, and checkouts do not persist credentials.
- The release job runs only for a `v*` tag on a commit that is on `main`, and whose version matches
  the package version.

## Reporting a Vulnerability

If you discover a security vulnerability in Minecraft Packs, please report it responsibly. Do not
create a public GitHub issue for security vulnerabilities.

**Contact:** GitHub Security Advisories (https://github.com/JudoChinX/minecraft-packs/security/advisories/new)

**Response Timeline:**
- **Acknowledgment:** You will receive an acknowledgment of your report within 48 hours.
- **Coordinated Disclosure:** We follow a 90-day coordinated disclosure timeline. Security fixes will
  be released before public disclosure whenever possible.

We appreciate responsible disclosure and will credit security researchers in release notes unless you
prefer to remain anonymous.
