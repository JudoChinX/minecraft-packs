"""Deterministic resource-pack zips, their SHA-1 sidecars, and structural verification.

The same entries always produce the same bytes: entries are sorted, stored uncompressed, stamped
with the zip epoch and mode 0644, and there are no directory entries. Storing rather than deflating
keeps the zip's bytes independent of the zlib build that happens to be installed; the PNGs inside
are already compressed, so little is lost. That makes a zip's SHA-1 a stable identity a server can
pin.
"""

import hashlib
import io
import json
import zipfile
import zlib
from pathlib import Path
from typing import Any

from PIL import Image
from PIL import UnidentifiedImageError

ICON_NAME = 'pack.png'
MCMETA_NAME = 'pack.mcmeta'
SHA1_SUFFIX = '.sha1'
ZIP_EPOCH = (1980, 1, 1, 0, 0, 0)

_FILE_MODE = 0o100644
_FORMAT_PARTS_MAX = 2
_MODE_SHIFT = 16
_PNG_SUFFIX = '.png'
_UNIX_SYSTEM = 3


def _check_entries(infos: list[zipfile.ZipInfo]) -> list[str]:
    """Report entries that break the deterministic layout."""
    names = [info.filename for info in infos]
    problems = [] if names == sorted(names) else ['entries are not sorted']
    for info in infos:
        if info.is_dir():
            problems.append(f'{info.filename}: directory entry')
        if info.date_time != ZIP_EPOCH:
            problems.append(f'{info.filename}: timestamp {info.date_time} is not the zip epoch')
        if info.compress_type != zipfile.ZIP_STORED:
            problems.append(f'{info.filename}: compressed; entries must be stored')
        if info.external_attr >> _MODE_SHIFT != _FILE_MODE:
            problems.append(f'{info.filename}: mode {info.external_attr >> _MODE_SHIFT:o} is not {_FILE_MODE:o}')
    return problems


def _check_icon(archive: zipfile.ZipFile) -> list[str]:
    """Report a missing or non-square ``pack.png``."""
    problems = []
    if ICON_NAME not in archive.namelist():
        problems.append(f'{ICON_NAME} is missing')
    else:
        size = _image_size(archive.read(ICON_NAME))
        if size is not None and size[0] != size[1]:
            problems.append(f'{ICON_NAME} is {size[0]}x{size[1]}, not square')
    return problems


def _check_mcmeta(archive: zipfile.ZipFile) -> list[str]:
    """Report a missing, unreadable or incomplete ``pack.mcmeta``."""
    try:
        problem = _mcmeta_problem(json.loads(archive.read(MCMETA_NAME).decode('utf-8')))
    except KeyError:
        problem = f'{MCMETA_NAME} is missing'
    except ValueError:
        problem = f'{MCMETA_NAME} is not valid UTF-8 JSON'
    return [problem] if problem else []


def _check_pngs(archive: zipfile.ZipFile) -> list[str]:
    """Report PNG entries that do not decode."""
    return [
        f'{name}: not a readable PNG'
        for name in archive.namelist()
        if name.endswith(_PNG_SUFFIX) and _image_size(archive.read(name)) is None
    ]


def _check_sidecar(zip_path: Path, digest: str) -> list[str]:
    """Report a ``.sha1`` sidecar that does not match the zip."""
    sidecar = sidecar_path(zip_path)
    problems = []
    if sidecar.is_file():
        recorded = sidecar.read_text(encoding='utf-8').split()
        if not recorded or recorded[0] != digest:
            problems.append(f'{sidecar.name} does not match the zip (zip SHA-1 is {digest})')
    return problems


def _image_size(data: bytes) -> tuple[int, int] | None:
    """Return a PNG's size, or None when it does not decode as a PNG."""
    try:
        with Image.open(io.BytesIO(data), formats=['PNG']) as image:
            image.load()
            size = image.size
    except (UnidentifiedImageError, OSError, SyntaxError):
        size = None
    return size


def _is_format(value: Any) -> bool:
    """Report whether a value is a pack format: an integer or a ``[major, minor]`` list."""
    parts = value if isinstance(value, list) and 1 <= len(value) <= _FORMAT_PARTS_MAX else [value]
    return all(isinstance(part, int) and not isinstance(part, bool) for part in parts)


def _mcmeta_problem(document: Any) -> str | None:
    """Describe what a parsed ``pack.mcmeta`` lacks, or return None when it is complete."""
    pack = document.get('pack') if isinstance(document, dict) else None
    problem = None
    if not isinstance(pack, dict):
        problem = f'{MCMETA_NAME} has no "pack" object'
    elif 'description' not in pack:
        problem = f'{MCMETA_NAME} has no pack description'
    elif not _is_format(pack.get('pack_format')) and not (
        _is_format(pack.get('min_format')) and _is_format(pack.get('max_format'))
    ):
        problem = f'{MCMETA_NAME} declares neither pack_format nor min_format and max_format'
    return problem


def sha1_hex(data: bytes) -> str:
    """Hash bytes the way Minecraft checks a server resource pack.

    SHA-1 is what the client verifies a downloaded pack against, so it is an integrity check here,
    not a security control.

    Args:
        data: The bytes to hash.

    Returns:
        The lowercase hexadecimal SHA-1 digest.
    """
    return hashlib.sha1(data, usedforsecurity=False).hexdigest()


def sidecar_path(zip_path: Path) -> Path:
    """Return where a zip's SHA-1 sidecar lives: beside it, with ``.sha1`` appended.

    Args:
        zip_path: The pack zip.

    Returns:
        The sidecar path, e.g. ``enchanter-0.1.0.zip.sha1``.
    """
    return zip_path.with_name(zip_path.name + SHA1_SUFFIX)


def verify_zip(zip_path: Path) -> list[str]:
    """Check a built pack zip without the network or the vanilla assets.

    Checks the deterministic layout, ``pack.mcmeta``, ``pack.png``, that every PNG decodes, and
    that a ``.sha1`` sidecar beside the zip, if present, matches it.

    Args:
        zip_path: The pack zip to check.

    Returns:
        Human-readable problems; empty when the zip is sound.
    """
    if not zip_path.is_file():
        return [f'{zip_path}: no such file']
    data = zip_path.read_bytes()
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            problems = _check_entries(archive.infolist())
            problems += _check_mcmeta(archive) + _check_icon(archive) + _check_pngs(archive)
    except (zipfile.BadZipFile, zlib.error):
        problems = ['not a zip file, or a corrupt one']
    return problems + _check_sidecar(zip_path, sha1_hex(data))


def write_zip(entries: dict[str, bytes], zip_path: Path) -> str:
    """Write a deterministic zip and its SHA-1 sidecar.

    Args:
        entries: File contents keyed by their path inside the zip.
        zip_path: Where to write the zip; its directory is created if needed.

    Returns:
        The zip's SHA-1.
    """
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_STORED) as archive:
        for name in sorted(entries):
            info = zipfile.ZipInfo(name, ZIP_EPOCH)
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = _FILE_MODE << _MODE_SHIFT
            info.create_system = _UNIX_SYSTEM
            archive.writestr(info, entries[name])
    data = buffer.getvalue()
    digest = sha1_hex(data)
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    zip_path.write_bytes(data)
    sidecar_path(zip_path).write_text(f'{digest}  {zip_path.name}\n', encoding='utf-8')
    return digest
