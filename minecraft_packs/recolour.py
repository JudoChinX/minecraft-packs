"""Palette-preserving hue-range recolouring of textures.

Every change is a rule matched against a colour's hue, saturation and lightness. A matching colour
takes the rule's target hue and saturation and keeps its own lightness (its shading, shifted by the
rule's offset) and its alpha. Nothing is hand-painted, so re-running the rules against a new vanilla
texture reproduces the look.
"""

import colorsys
from dataclasses import dataclass

from PIL import Image

type Rgb = tuple[int, int, int]

_CHANNEL_MAX = 255
_DEGREES = 360
_PALETTE_MODE = 'P'
_RGB_CHANNELS = 3


@dataclass(frozen=True)
class Rule:
    """One hue-range recolour rule.

    Ranges are inclusive. Hue is in degrees; saturation and lightness are HLS fractions from 0 to 1.
    """

    hue: tuple[float, float]
    lightness: tuple[float, float]
    lightness_offset: float
    name: str
    saturation: tuple[float, float]
    target_hue: float
    target_saturation: float

    def matches(self, hue_degrees: float, lightness: float, saturation: float) -> bool:
        """Report whether a colour falls inside all three of this rule's ranges.

        Args:
            hue_degrees: The colour's hue in degrees.
            lightness: The colour's HLS lightness.
            saturation: The colour's HLS saturation.

        Returns:
            True when hue, saturation and lightness are each within range.
        """
        return (
            self.hue[0] <= hue_degrees <= self.hue[1]
            and self.saturation[0] <= saturation <= self.saturation[1]
            and self.lightness[0] <= lightness <= self.lightness[1]
        )


def _hls(rgb: Rgb) -> tuple[float, float, float]:
    """Convert an 8-bit RGB colour to HLS fractions."""
    return colorsys.rgb_to_hls(*(channel / _CHANNEL_MAX for channel in rgb))


def match_rule(rgb: Rgb, rules: tuple[Rule, ...]) -> Rule | None:
    """Find the first rule that matches a colour.

    Args:
        rgb: An 8-bit RGB colour.
        rules: Rules in priority order.

    Returns:
        The first matching rule, or None when the colour matches no rule and is left untouched.
    """
    hue, lightness, saturation = _hls(rgb)
    return next((rule for rule in rules if rule.matches(hue * _DEGREES, lightness, saturation)), None)


def recolour_image(image: Image.Image, rules: tuple[Rule, ...]) -> tuple[Image.Image, dict[str, int]]:
    """Recolour a texture, keeping its size, mode, shading and transparency.

    A palette image has its palette edited in place, so pixel indices, transparency and mode are
    unchanged. Any other image is converted to RGBA and recoloured per opaque pixel.

    Args:
        image: The vanilla texture.
        rules: Rules in priority order.

    Returns:
        The recoloured image and, per rule name, how many palette entries (or pixels) it changed.
    """
    counts: dict[str, int] = {}
    if image.mode == _PALETTE_MODE:
        result = image.copy()
        palette = result.getpalette()
        transparent = result.info.get('transparency')
        for index in range(len(palette) // _RGB_CHANNELS):
            start = index * _RGB_CHANNELS
            new_rgb, name = recolour_rgb(tuple(palette[start : start + _RGB_CHANNELS]), rules)
            if name and index != transparent:
                palette[start : start + _RGB_CHANNELS] = new_rgb
                counts[name] = counts.get(name, 0) + 1
        result.putpalette(palette)
    else:
        result = image.convert('RGBA')
        pixels = result.load()
        for row in range(result.height):
            for col in range(result.width):
                red, green, blue, alpha = pixels[col, row]
                new_rgb, name = recolour_rgb((red, green, blue), rules)
                if name and alpha:
                    pixels[col, row] = (*new_rgb, alpha)
                    counts[name] = counts.get(name, 0) + 1
    return result, counts


def recolour_rgb(rgb: Rgb, rules: tuple[Rule, ...]) -> tuple[Rgb, str | None]:
    """Recolour one colour by the first rule that matches it.

    Args:
        rgb: An 8-bit RGB colour.
        rules: Rules in priority order.

    Returns:
        The new colour and the matching rule's name, or the colour unchanged and None.
    """
    rule = match_rule(rgb, rules)
    red, green, blue = rgb
    if rule is not None:
        _, lightness, _ = _hls(rgb)
        shifted = min(max(lightness + rule.lightness_offset, 0.0), 1.0)
        channels = colorsys.hls_to_rgb(rule.target_hue / _DEGREES, shifted, rule.target_saturation)
        red, green, blue = (round(channel * _CHANNEL_MAX) for channel in channels)
    return (red, green, blue), rule.name if rule else None
