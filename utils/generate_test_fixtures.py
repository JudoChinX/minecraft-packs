"""Generate the synthetic palette texture the tests build packs from.

The tests never use Mojang's assets. This writes a 64 x 64, 8-bit palette PNG shaped like an entity
texture: index 0 is transparent, and each other palette entry is a colour chosen to exercise one
recolour rule or to be left untouched. Run it from the repository root:

    python utils/generate_test_fixtures.py
"""

from pathlib import Path

from PIL import Image

FIXTURE_PATH = Path('tests/fixtures/palette-64.png')
PALETTE = [
    (0, 0, 0),  # transparent
    (40, 70, 160),  # saturated blue: robe
    (170, 190, 215),  # pale blue: trim
    (40, 150, 150),  # teal: amber
    (110, 80, 200),  # blue-violet: pale
    (150, 150, 150),  # grey skin: untouched
    (50, 50, 60),  # dark shirt: untouched
    (60, 160, 60),  # green eyes: untouched
]
SIZE = 64
BAND_HEIGHT = SIZE // len(PALETTE)


def main() -> None:
    """Write the fixture, one horizontal band per palette entry."""
    image = Image.new('P', (SIZE, SIZE))
    image.putpalette([channel for colour in PALETTE for channel in colour])
    image.putdata([row // BAND_HEIGHT for row in range(SIZE) for _ in range(SIZE)])
    FIXTURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    image.save(FIXTURE_PATH, format='PNG', optimize=False, transparency=0)
    print(FIXTURE_PATH)


if __name__ == '__main__':
    main()
