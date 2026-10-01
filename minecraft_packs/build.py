"""Assemble packs: recolour vanilla textures, add static files, write the zip, and render previews."""

import io
import json
import logging
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

from minecraft_packs.archive import ICON_NAME
from minecraft_packs.archive import MCMETA_NAME
from minecraft_packs.archive import sidecar_path
from minecraft_packs.archive import verify_zip
from minecraft_packs.archive import write_zip
from minecraft_packs.config import PackConfig
from minecraft_packs.errors import PackError
from minecraft_packs.models import MODELS
from minecraft_packs.recolour import recolour_image
from minecraft_packs.render import icon
from minecraft_packs.render import preview_sheet
from minecraft_packs.vanilla import fetch_client_jar
from minecraft_packs.vanilla import read_asset
from minecraft_packs.vanilla import verify_client_jar

_ZIP_SUFFIX = '.zip'

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class BuildResult:
    """What a build produced."""

    counts: dict[str, dict[str, int]]
    sha1: str
    size: int
    zip_path: Path


def _encode_png(image: Image.Image) -> bytes:
    """Encode an image as PNG, keeping a palette image's transparency."""
    buffer = io.BytesIO()
    options = {'transparency': image.info['transparency']} if 'transparency' in image.info else {}
    image.save(buffer, format='PNG', optimize=False, **options)
    return buffer.getvalue()


def _static_files(pack: PackConfig) -> dict[str, bytes]:
    """Read the pack's verbatim files, keyed by their path inside the zip, skipping dotfiles."""
    files = sorted(path for path in pack.files_dir.rglob('*') if path.is_file()) if pack.files_dir.is_dir() else []
    relative = [path.relative_to(pack.files_dir) for path in files]
    return {
        name.as_posix(): path.read_bytes()
        for name, path in zip(relative, files, strict=True)
        if not any(part.startswith('.') for part in name.parts)
    }


def _check_data_files(name: str, files: dict[str, bytes]) -> None:
    """Refuse a data pack file outside ``data/`` (``pack.png`` aside), or JSON that does not parse."""
    for path, data in sorted(files.items()):
        if path != ICON_NAME and not path.startswith('data/'):
            raise PackError(f'{name}: a data pack keeps its files under files/data/, not {path}.')
        if path.endswith('.json'):
            try:
                json.loads(data)
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                raise PackError(f'{name}: files/{path} is not valid JSON: {error}') from error


def build_pack(
    pack: PackConfig,
    version: str,
    out_dir: Path,
    cache_dir: Path,
    client_jar: Path | None = None,
) -> BuildResult:
    """Build one pack into ``<out_dir>/<name>-<version>.zip`` with a ``.sha1`` beside it.

    Args:
        pack: The pack definition.
        version: The release version, used in the zip's name.
        out_dir: Where to write the zip and its sidecar.
        cache_dir: Where the client jar is cached.
        client_jar: A local client jar to use instead of downloading one; still verified.

    Returns:
        The zip's path, size and SHA-1, and how many colours each rule changed per texture.

    Raises:
        PackError: If the vanilla assets cannot be obtained or verified, the pack is incomplete, or
            the zip fails verification (in which case the zip and its sidecar are removed).
    """
    vanilla = vanilla_textures(pack, cache_dir, client_jar)
    entries, counts = pack_entries(pack, vanilla)
    zip_path = out_dir / f'{pack.name}-{version}{_ZIP_SUFFIX}'
    digest = write_zip(entries, zip_path)
    problems = verify_zip(zip_path)
    if problems:
        zip_path.unlink()
        sidecar_path(zip_path).unlink()
        raise PackError(f'{zip_path} failed verification: {"; ".join(problems)}')
    return BuildResult(counts=counts, sha1=digest, size=zip_path.stat().st_size, zip_path=zip_path)


def pack_entries(
    pack: PackConfig,
    vanilla: dict[str, Image.Image],
) -> tuple[dict[str, bytes], dict[str, dict[str, int]]]:
    """Produce every file of a pack, keyed by its path inside the zip.

    Args:
        pack: The pack definition.
        vanilla: The vanilla textures, keyed by asset path.

    Returns:
        The pack's files, and per texture how many colours each rule changed.

    Raises:
        PackError: If a static file would overwrite a generated one, or the pack has no icon.
    """
    entries: dict[str, bytes] = {MCMETA_NAME: (json.dumps(pack.mcmeta(), indent=2, ensure_ascii=False) + '\n').encode()}
    counts: dict[str, dict[str, int]] = {}
    recoloured: dict[str, Image.Image] = {}
    for texture in pack.textures:
        recoloured[texture.path], counts[texture.path] = recolour_image(vanilla[texture.path], texture.rules)
        entries[texture.path] = _encode_png(recoloured[texture.path])
    if pack.preview is not None:
        entries[ICON_NAME] = _encode_png(icon(recoloured[pack.preview.texture], MODELS[pack.preview.model]))
    static = _static_files(pack)
    clashes = sorted(set(static) & set(entries))
    if clashes:
        raise PackError(f'{pack.name}: files/ would overwrite generated file(s): {", ".join(clashes)}.')
    if pack.kind == 'data':
        _check_data_files(pack.name, static)
    entries.update(static)
    if ICON_NAME not in entries:
        raise PackError(f'{pack.name}: no {ICON_NAME}; add a [preview] to generate one, or files/{ICON_NAME}.')
    return entries, counts


def preview_pack(pack: PackConfig, out_path: Path, cache_dir: Path, client_jar: Path | None = None) -> Path:
    """Render a pack's review sheet: its recoloured texture and front view, side by side.

    The vanilla texture is read only to recolour it; it is not drawn.

    Args:
        pack: The pack definition; it must have a ``[preview]``.
        out_path: Where to write the PNG.
        cache_dir: Where the client jar is cached.
        client_jar: A local client jar to use instead of downloading one; still verified.

    Returns:
        The path written.

    Raises:
        PackError: If the pack has no ``[preview]`` or its vanilla assets cannot be obtained.
    """
    if pack.preview is None:
        raise PackError(f'{pack.name}: no [preview] in its pack.toml, so there is nothing to preview.')
    texture = next(texture for texture in pack.textures if texture.path == pack.preview.texture)
    original = vanilla_textures(pack, cache_dir, client_jar)[texture.path]
    recoloured, _ = recolour_image(original, texture.rules)
    sheet = preview_sheet(recoloured, MODELS[pack.preview.model], pack.preview.title)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path, format='PNG')
    return out_path


def record_expected_sha1(pack: PackConfig, digest: str) -> Path:
    """Record a build's SHA-1 as the one the pack is expected to produce.

    Args:
        pack: The pack definition.
        digest: The SHA-1 of the pack's newly built zip.

    Returns:
        The path written, ``packs/<name>/expected.sha1``.
    """
    pack.expected_sha1_path.write_text(f'{digest}\n', encoding='utf-8')
    return pack.expected_sha1_path


def vanilla_textures(pack: PackConfig, cache_dir: Path, client_jar: Path | None = None) -> dict[str, Image.Image]:
    """Read and verify the vanilla textures a pack recolours.

    Args:
        pack: The pack definition.
        cache_dir: Where the client jar is cached.
        client_jar: A local client jar to use instead of downloading one; still verified.

    Returns:
        The vanilla textures keyed by asset path; empty when the pack recolours nothing.

    Raises:
        PackError: If the client jar or any texture fails verification.
    """
    textures: dict[str, Image.Image] = {}
    if pack.vanilla is not None and pack.textures:
        if client_jar is not None:
            jar_path = verify_client_jar(client_jar, pack.vanilla)
        else:
            jar_path = fetch_client_jar(pack.vanilla, cache_dir)
        for texture in pack.textures:
            data = read_asset(jar_path, texture.path, texture.sha256)
            textures[texture.path] = Image.open(io.BytesIO(data), formats=['PNG'])
    return textures
