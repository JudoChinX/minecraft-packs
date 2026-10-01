"""Command-line interface: ``python -m minecraft_packs build|preview|verify``.

Run it from the repository root. Results a script might consume (zip paths and SHA-1s) go to
standard output; progress and errors go to standard error.
"""

import argparse
import logging
import sys
from pathlib import Path

from minecraft_packs import __version__
from minecraft_packs.archive import sha1_hex
from minecraft_packs.archive import verify_zip
from minecraft_packs.build import build_pack
from minecraft_packs.build import preview_pack
from minecraft_packs.build import record_expected_sha1
from minecraft_packs.config import load_packs
from minecraft_packs.errors import PackError

DEFAULT_CACHE_DIR = Path('.cache')
DEFAULT_OUT_DIR = Path('dist')
DEFAULT_PACKS_DIR = Path('packs')

logger = logging.getLogger(__name__)


def _add_source_options(parser: argparse.ArgumentParser) -> None:
    """Add the options that say where pack definitions and vanilla assets come from."""
    parser.add_argument(
        '--packs-dir', type=Path, default=DEFAULT_PACKS_DIR, help='directory of pack definitions (default: packs)'
    )
    parser.add_argument('--cache-dir', type=Path, default=DEFAULT_CACHE_DIR, help='client jar cache (default: .cache)')
    parser.add_argument(
        '--client-jar',
        type=Path,
        default=None,
        help='use this Minecraft client jar instead of downloading one; it must match the pinned SHA-1',
    )


def _build(args: argparse.Namespace) -> int:
    """Build the requested packs, print each zip's path and SHA-1, and compare it with the pin."""
    mismatched = []
    for pack in load_packs(args.packs_dir, args.packs):
        result = build_pack(pack, __version__, args.out_dir, args.cache_dir, args.client_jar)
        for texture, counts in result.counts.items():
            logger.info(f'{pack.name}: {texture}: recoloured {counts}')
        print(f'{result.zip_path} ({result.size} bytes)')
        # A resource pack's line is the server setting it pins; a data pack has no such setting.
        print(f'{"RESOURCE_PACK_SHA1" if pack.kind == "resource" else "DATA_PACK_SHA1"}={result.sha1}')
        if args.update_expected:
            logger.info(f'{pack.name}: recorded {record_expected_sha1(pack, result.sha1)}')
        elif result.sha1 != pack.expected_sha1:
            mismatched.append(pack.name)
            logger.log(
                logging.ERROR if args.check else logging.WARNING,
                f'{pack.name}: SHA-1 {result.sha1} does not match {pack.expected_sha1_path} '
                f'({pack.expected_sha1 or "missing"}). If the change is intended, rebuild with --update-expected.',
            )
    return 1 if args.check and mismatched else 0


def _parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        prog='python -m minecraft_packs',
        description='Build Minecraft Java resource packs reproducibly from official assets.',
    )
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    commands = parser.add_subparsers(dest='command', required=True)

    build = commands.add_parser('build', help='build packs into deterministic zips with .sha1 sidecars')
    build.add_argument('packs', nargs='*', metavar='PACK', help='packs to build (default: all)')
    build.add_argument('--out-dir', type=Path, default=DEFAULT_OUT_DIR, help='output directory (default: dist)')
    pin = build.add_mutually_exclusive_group()
    pin.add_argument('--check', action='store_true', help="fail unless each zip matches its pack's expected.sha1")
    pin.add_argument('--update-expected', action='store_true', help="record each zip's SHA-1 in its expected.sha1")
    _add_source_options(build)
    build.set_defaults(handler=_build)

    preview = commands.add_parser('preview', help="render a review sheet of a pack's texture and front view")
    preview.add_argument('pack', metavar='PACK', help='the pack to preview')
    preview.add_argument('out', type=Path, metavar='OUT', help='the PNG to write')
    _add_source_options(preview)
    preview.set_defaults(handler=_preview)

    verify = commands.add_parser('verify', help='check built zips and their .sha1 sidecars, offline')
    verify.add_argument('zips', nargs='+', type=Path, metavar='ZIP', help='zips to check')
    verify.set_defaults(handler=_verify)
    return parser


def _preview(args: argparse.Namespace) -> int:
    """Render one pack's review sheet and print its path."""
    pack = load_packs(args.packs_dir, [args.pack])[0]
    print(preview_pack(pack, args.out, args.cache_dir, args.client_jar))
    return 0


def _verify(args: argparse.Namespace) -> int:
    """Verify each zip, printing its SHA-1 when sound and its problems when not."""
    failed = 0
    for zip_path in args.zips:
        problems = verify_zip(zip_path)
        for problem in problems:
            logger.error(f'{zip_path}: {problem}')
        if problems:
            failed += 1
        else:
            print(f'{zip_path}: OK sha1={sha1_hex(zip_path.read_bytes())}')
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    """Run the command line.

    Args:
        argv: Arguments without the program name; defaults to ``sys.argv[1:]``.

    Returns:
        The process exit status: 0 on success, 1 on any failure.
    """
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s', stream=sys.stderr)
    args = _parser().parse_args(argv)
    try:
        status = args.handler(args)
    except PackError as error:
        logger.error(str(error))
        status = 1
    return status
