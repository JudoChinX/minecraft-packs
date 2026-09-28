"""Render front views, pack icons and review sheets from entity textures."""

import math

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from minecraft_packs.models import Layout

ICON_SIZE = 64

_BACKGROUND = (40, 40, 46, 255)
_CHECKER_CELL = 16
_CHECKER_DARK = (90, 90, 96, 255)
_CHECKER_LIGHT = (110, 110, 118, 255)
_FOOTER_FONT_SIZE = 16
_FOOTER_HEIGHT = 30
_FOOTER_TEXT = (180, 180, 190, 255)
_FRONT_SCALE = 12
_LABEL_HEIGHT = 40
_PADDING = 24
_TEXTURE_SCALE = 8
_TITLE_FONT_SIZE = 22
_TITLE_OFFSET = 6
_TITLE_TEXT = (235, 235, 240, 255)
_TRANSPARENT = (0, 0, 0, 0)


def _checker(size: tuple[int, int]) -> Image.Image:
    """Draw a transparency checkerboard of the given size."""
    board = Image.new('RGBA', size, _CHECKER_DARK)
    draw = ImageDraw.Draw(board)
    for top in range(0, size[1], _CHECKER_CELL):
        for left in range(0, size[0], _CHECKER_CELL):
            if (left // _CHECKER_CELL + top // _CHECKER_CELL) % 2:
                draw.rectangle((left, top, left + _CHECKER_CELL - 1, top + _CHECKER_CELL - 1), fill=_CHECKER_LIGHT)
    return board


def _scaled(image: Image.Image, scale: int) -> Image.Image:
    """Upscale an image by an integer factor without smoothing."""
    return image.convert('RGBA').resize((image.width * scale, image.height * scale), Image.Resampling.NEAREST)


def front_view(texture: Image.Image, layout: Layout) -> Image.Image:
    """Paint a model's flat front view from its texture.

    Args:
        texture: The entity texture, in any mode.
        layout: The model's front-view layout.

    Returns:
        An RGBA image of ``layout.canvas`` size.
    """
    rgba = texture.convert('RGBA')
    canvas = Image.new('RGBA', layout.canvas, _TRANSPARENT)
    for part in layout.parts:
        canvas.alpha_composite(part.front(rgba), (layout.origin[0] + part.offset[0], layout.origin[1] + part.offset[1]))
    return canvas


def icon(texture: Image.Image, layout: Layout) -> Image.Image:
    """Make a ``pack.png`` icon: the model's face, upscaled to the icon size.

    Args:
        texture: The entity texture.
        layout: The model's front-view layout.

    Returns:
        An RGBA image of ``ICON_SIZE`` by ``ICON_SIZE`` pixels.
    """
    face = front_view(texture, layout).crop(layout.icon_box)
    return face.resize((ICON_SIZE, ICON_SIZE), Image.Resampling.NEAREST)


def preview_sheet(recoloured: Image.Image, layout: Layout, title: str) -> Image.Image:
    """Draw a pack's texture and its model's front view side by side for review.

    Only the pack's derived texture is drawn, never the vanilla one.

    Args:
        recoloured: The pack's texture.
        layout: The model's front-view layout.
        title: The pack's name for the mob, e.g. ``Enchanter``.

    Returns:
        An RGB review sheet.
    """
    panels = [
        (f'{title} (texture x{_TEXTURE_SCALE})', _scaled(recoloured, _TEXTURE_SCALE)),
        (f'{title} front', _scaled(front_view(recoloured, layout), _FRONT_SCALE)),
    ]
    title_font = ImageFont.load_default(size=_TITLE_FONT_SIZE)
    footer_font = ImageFont.load_default(size=_FOOTER_FONT_SIZE)
    footer = f'Front view: a rough flat layout of the model ({layout.summary}), not an in-game render.'
    columns = [max(panel.width, math.ceil(title_font.getlength(label))) for label, panel in panels]
    width = max(
        _PADDING + sum(column + _PADDING for column in columns), 2 * _PADDING + math.ceil(footer_font.getlength(footer))
    )
    height = _PADDING + _LABEL_HEIGHT + max(panel.height for _, panel in panels) + _PADDING + _FOOTER_HEIGHT
    sheet = Image.new('RGBA', (width, height), _BACKGROUND)
    draw = ImageDraw.Draw(sheet)
    left = _PADDING
    for (label, panel), column in zip(panels, columns, strict=True):
        board = _checker(panel.size)
        board.alpha_composite(panel)
        sheet.alpha_composite(board, (left, _PADDING + _LABEL_HEIGHT))
        draw.text((left, _PADDING + _TITLE_OFFSET), label, fill=_TITLE_TEXT, font=title_font)
        left += column + _PADDING
    draw.text((_PADDING, height - _FOOTER_HEIGHT), footer, fill=_FOOTER_TEXT, font=footer_font)
    return sheet.convert('RGB')
