"""Flat front-view layouts of vanilla entity models, used for previews and pack icons.

A layout places the front face of each of a model's boxes on a small canvas. It is a rough, flat
picture of the model for review, not an in-game render. UVs follow the vanilla model classes.
"""

from dataclasses import dataclass

from PIL import Image


@dataclass(frozen=True)
class Part:
    """One model box: its texture offset, size, and where its front face sits on the canvas."""

    depth: int
    height: int
    mirrored: bool
    offset: tuple[int, int]
    uv: tuple[int, int]
    width: int

    def front(self, texture: Image.Image) -> Image.Image:
        """Crop this box's front face from a texture.

        Args:
            texture: The entity texture, in RGBA.

        Returns:
            The front face, mirrored left to right when the part is mirrored.
        """
        left = self.uv[0] + self.depth
        top = self.uv[1] + self.depth
        face = texture.crop((left, top, left + self.width, top + self.height))
        return face.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if self.mirrored else face


@dataclass(frozen=True)
class Layout:
    """A model's flat front view: canvas size, model origin, parts in paint order, and icon crop."""

    canvas: tuple[int, int]
    icon_box: tuple[int, int, int, int]
    origin: tuple[int, int]
    parts: tuple[Part, ...]
    summary: str


def _part(uv: tuple[int, int], size: tuple[int, int, int], offset: tuple[int, int], mirrored: bool = False) -> Part:
    """Build a part from a texture offset, a (width, height, depth) size and a canvas offset."""
    return Part(depth=size[2], height=size[1], mirrored=mirrored, offset=offset, uv=uv, width=size[0])


# Illager boxes from vanilla IllagerModel; the model origin is the neck centre, y grows downwards.
_ILLAGER = Layout(
    canvas=(16, 34),
    icon_box=(4, 1, 12, 9),
    origin=(8, 10),
    parts=(
        _part((0, 22), (4, 12, 4), (-4, 12)),
        _part((0, 22), (4, 12, 4), (0, 12), mirrored=True),
        _part((16, 20), (8, 12, 6), (-4, 0)),
        _part((0, 38), (8, 20, 6), (-4, 0)),
        _part((0, 0), (8, 10, 8), (-4, -10)),
        _part((24, 0), (2, 4, 2), (-1, -3)),
        _part((32, 0), (8, 12, 8), (-4, -10)),
        _part((44, 22), (4, 8, 4), (-8, 1)),
        _part((44, 22), (4, 8, 4), (4, 1), mirrored=True),
        _part((40, 38), (8, 4, 4), (-4, 5)),
    ),
    summary='legs, robe, head, hood, crossed arms',
)

MODELS: dict[str, Layout] = {
    'illager': _ILLAGER,
}
