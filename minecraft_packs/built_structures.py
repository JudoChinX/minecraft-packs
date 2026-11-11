"""The built-structures bundle: ``built-structures/`` zipped deterministically for a release.

The Mobs plugin reads the bundle as a stored zip of flat ``built_<id>.nbt`` and ``built_<id>.json`` pairs, each
id once and at most 50 of them. It reuses the pack zip layout (sorted, stored, zip epoch, mode 0644), so the
same files always give the same bytes and the same SHA-256. A directory the plugin would refuse fails here, so
CI stops before a release rather than the server pausing every Send.
"""

import re
from pathlib import Path

from minecraft_packs.archive import zip_flat
from minecraft_packs.errors import PackError

MAX_STRUCTURES = 50

_ENTRY = re.compile(r'built_[a-z0-9]+(_[a-z0-9]+)*\.(nbt|json)')


def zip_bundle(src: Path, out: Path) -> str:
    """Zip the built structures in a directory and write the zip's SHA-256 file beside it.

    Only top-level files named ``built_<id>.nbt`` or ``built_<id>.json`` go in; the README and anything
    else is left out. A directory with none gives a valid, empty zip.

    Args:
        src: The ``built-structures/`` directory.
        out: Where to write the zip; its directory is created if needed.

    Returns:
        The zip's SHA-256.

    Raises:
        PackError: A ``.nbt`` has no ``.json`` or the reverse, or there are more than 50 structures.
    """
    digest, names = zip_flat(src, out, _ENTRY)
    kinds: dict[str, set[str]] = {}
    for name in names:
        stem, _, kind = name.rpartition('.')
        kinds.setdefault(stem, set()).add(kind)
    unpaired = sorted(stem for stem, found in kinds.items() if len(found) != 2)
    if unpaired:
        raise PackError(f'{src}: needs both .nbt and .json: {", ".join(unpaired)}')
    if len(kinds) > MAX_STRUCTURES:
        raise PackError(f'{src}: {len(kinds)} structures; the limit is {MAX_STRUCTURES}')
    return digest
