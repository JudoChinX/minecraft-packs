"""Tests for models.py and render.py: front faces, front views, icons and review sheets."""

import pytest
from PIL import Image

from minecraft_packs.models import MODELS
from minecraft_packs.models import Layout
from minecraft_packs.models import Part
from minecraft_packs.render import ICON_SIZE
from minecraft_packs.render import front_view
from minecraft_packs.render import icon
from minecraft_packs.render import preview_sheet
from tests.helpers import FIXTURE_PATH

_ILLAGER = MODELS['illager']

_front_cases = {
    'mirrored': {'mirrored': True, 'expected': [(2, 1), (1, 1), (2, 2), (1, 2)]},
    'plain': {'mirrored': False, 'expected': [(1, 1), (2, 1), (1, 2), (2, 2)]},
}


def _coordinate_texture() -> Image.Image:
    """Build a 4 x 4 texture whose every pixel encodes its own coordinates."""
    texture = Image.new('RGBA', (4, 4))
    for row in range(4):
        for col in range(4):
            texture.putpixel((col, row), (col, row, 0, 255))
    return texture


def _fixture() -> Image.Image:
    """Load the synthetic palette texture."""
    with Image.open(FIXTURE_PATH) as texture:
        texture.load()
    return texture


@pytest.mark.parametrize(
    'mirrored, expected',
    [(case['mirrored'], case['expected']) for case in _front_cases.values()],
    ids=list(_front_cases.keys()),
)
def test_front(mirrored: bool, expected: list[tuple[int, int]]) -> None:
    """Test Part.front crops the box's front face, offset by its depth, mirrored on request."""
    part = Part(depth=1, height=2, mirrored=mirrored, offset=(0, 0), uv=(0, 0), width=2)

    face = part.front(_coordinate_texture())

    assert [pixel[:2] for pixel in face.get_flattened_data()] == expected


def test_front_view_paints_parts_in_order_at_their_offsets() -> None:
    """Test later parts paint over earlier ones, placed relative to the origin."""
    texture = Image.new('RGBA', (4, 4), (255, 0, 0, 255))
    texture.putpixel((3, 3), (0, 0, 255, 255))
    layout = Layout(
        canvas=(3, 3),
        icon_box=(0, 0, 1, 1),
        origin=(1, 1),
        parts=(
            Part(depth=0, height=2, mirrored=False, offset=(-1, -1), uv=(0, 0), width=2),
            Part(depth=0, height=1, mirrored=False, offset=(0, 0), uv=(3, 3), width=1),
        ),
        summary='test',
    )

    view = front_view(texture, layout)

    assert view.getpixel((0, 0)) == (255, 0, 0, 255)
    assert view.getpixel((1, 1)) == (0, 0, 255, 255)
    assert view.getpixel((2, 2)) == (0, 0, 0, 0)


def test_front_view_is_canvas_sized_rgba() -> None:
    """Test the illager front view has the layout's canvas size and is RGBA."""
    view = front_view(_fixture(), _ILLAGER)

    assert (view.mode, view.size) == ('RGBA', _ILLAGER.canvas)


def test_icon_is_square_icon_size() -> None:
    """Test the pack icon is the face crop upscaled to the icon size."""
    result = icon(_fixture(), _ILLAGER)

    assert result.size == (ICON_SIZE, ICON_SIZE)


def test_preview_sheet_lays_out_two_panels() -> None:
    """Test the review sheet is RGB and sized for one x8 texture and one x12 front view."""
    sheet = preview_sheet(_fixture(), _ILLAGER, 'Test')

    assert sheet.mode == 'RGB'
    assert sheet.height == 24 + 40 + 512 + 24 + 30
    assert sheet.width >= 24 + (512 + 24) + (16 * 12 + 24)


def test_preview_sheet_widens_for_long_labels() -> None:
    """Test a long title widens its column instead of being clipped."""
    short = preview_sheet(_fixture(), _ILLAGER, 'Test')
    long = preview_sheet(_fixture(), _ILLAGER, 'A very long mob name for the preview sheet')

    assert long.width > short.width
