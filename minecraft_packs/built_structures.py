"""The built-structures bundle: ``built-structures/`` zipped deterministically for a release.

The Mobs plugin reads the bundle as a stored zip of flat ``built_*.nbt`` and ``built_*.json`` entries, one
pair per structure. It reuses the pack zip layout (sorted, stored, zip epoch, mode 0644), so the same files
always give the same bytes and the same SHA-256.
"""

import hashlib
import re
from pathlib import Path

from minecraft_packs.archive import write_zip
from minecraft_packs.built_mobs import sha256_path

_ENTRY = re.compile(r'built_[a-z0-9_]+\.(nbt|json)')


def zip_bundle(src: Path, out: Path) -> str:
    """Zip the built structures in a directory and write the zip's SHA-256 file beside it.

    Only top-level files named ``built_<id>.nbt`` or ``built_<id>.json`` go in; the README and anything
    else is left out. A directory with none gives a valid, empty zip.

    Args:
        src: The ``built-structures/`` directory.
        out: Where to write the zip; its directory is created if needed.

    Returns:
        The zip's SHA-256.
    """
    entries = {path.name: path.read_bytes() for path in src.iterdir() if path.is_file() and _ENTRY.fullmatch(path.name)}
    write_zip(entries, out)
    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    sha256_path(out).write_text(f'{digest}  {out.name}\n', encoding='utf-8')
    return digest
