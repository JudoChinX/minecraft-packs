"""The built-mobs bundle: ``built-mobs/`` zipped deterministically for a release.

The Mobs plugin reads the bundle as a stored zip of flat ``built_*.json`` and ``built_*.bbmodel`` entries.
It reuses the pack zip layout (sorted, stored, zip epoch, mode 0644), so the same files always give the
same bytes and the same SHA-256.
"""

import hashlib
import re
from pathlib import Path

from minecraft_packs.archive import write_zip

SHA256_SUFFIX = '.sha256'

_ENTRY = re.compile(r'built_[a-z0-9_]+\.(json|bbmodel)')


def sha256_path(zip_path: Path) -> Path:
    """Return where a bundle's SHA-256 file lives: beside it, ``.zip`` replaced by ``.sha256``.

    Args:
        zip_path: The bundle zip.

    Returns:
        The SHA-256 file path, e.g. ``dist/built-mobs.sha256``.
    """
    return zip_path.with_suffix(SHA256_SUFFIX)


def zip_bundle(src: Path, out: Path) -> str:
    """Zip the built mobs in a directory and write the zip's SHA-256 file beside it.

    Only top-level files named ``built_<id>.json`` or ``built_<id>.bbmodel`` go in; the README and anything
    else is left out. A directory with none gives a valid, empty zip.

    Args:
        src: The ``built-mobs/`` directory.
        out: Where to write the zip; its directory is created if needed.

    Returns:
        The zip's SHA-256.
    """
    entries = {path.name: path.read_bytes() for path in src.iterdir() if path.is_file() and _ENTRY.fullmatch(path.name)}
    write_zip(entries, out)
    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    sha256_path(out).write_text(f'{digest}  {out.name}\n', encoding='utf-8')
    return digest
