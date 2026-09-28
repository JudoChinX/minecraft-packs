"""Allow the package to be run as ``python -m minecraft_packs``."""

import sys

from minecraft_packs.cli import main

if __name__ == '__main__':
    sys.exit(main())
