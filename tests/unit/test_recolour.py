"""Tests for recolour.py: rule matching, colour recolouring and whole-texture recolouring."""

import pytest
from PIL import Image

from minecraft_packs.recolour import Rgb
from minecraft_packs.recolour import Rule
from minecraft_packs.recolour import match_rule
from minecraft_packs.recolour import recolour_image
from minecraft_packs.recolour import recolour_rgb
from tests.builders import RuleBuilder
from tests.helpers import FIXTURE_PATH

_RULES = (
    RuleBuilder().robe().build(),
    RuleBuilder().trim().build(),
    RuleBuilder().amber().build(),
    RuleBuilder().pale().build(),
)

_match_rule_cases = {
    'first_match_wins': {
        'rgb': (40, 70, 160),
        'rules': (RuleBuilder().named('first').build(), RuleBuilder().named('second').build()),
        'expected': 'first',
    },
    'no_rules': {
        'rgb': (40, 70, 160),
        'rules': (),
        'expected': None,
    },
    'teal_matches_amber': {
        'rgb': (40, 150, 150),
        'rules': _RULES,
        'expected': 'amber',
    },
}

_matches_cases = {
    'hue_above': {'rule': RuleBuilder().robe().build(), 'hls': (240.1, 0.5, 0.5), 'expected': False},
    'hue_below': {'rule': RuleBuilder().robe().build(), 'hls': (189.9, 0.5, 0.5), 'expected': False},
    'hue_lower_bound': {'rule': RuleBuilder().robe().build(), 'hls': (190.0, 0.5, 0.5), 'expected': True},
    'hue_upper_bound': {'rule': RuleBuilder().robe().build(), 'hls': (240.0, 0.5, 0.5), 'expected': True},
    'inside': {'rule': RuleBuilder().robe().build(), 'hls': (215.0, 0.5, 0.5), 'expected': True},
    'lightness_below': {'rule': RuleBuilder().trim().build(), 'hls': (215.0, 0.44, 0.2), 'expected': False},
    'saturation_below': {'rule': RuleBuilder().robe().build(), 'hls': (215.0, 0.5, 0.39), 'expected': False},
    'saturation_upper_bound': {'rule': RuleBuilder().trim().build(), 'hls': (215.0, 0.5, 0.4), 'expected': True},
}

_recolour_rgb_cases = {
    'blue_violet_to_pale_gold': {'rgb': (110, 80, 200), 'expected': ((242, 231, 161), 'pale')},
    'dark_shirt_untouched': {'rgb': (50, 50, 60), 'expected': ((50, 50, 60), None)},
    'green_eyes_untouched': {'rgb': (60, 160, 60), 'expected': ((60, 160, 60), None)},
    'grey_skin_untouched': {'rgb': (150, 150, 150), 'expected': ((150, 150, 150), None)},
    'lightness_clamped_to_white': {'rgb': (200, 190, 250), 'expected': ((255, 255, 255), 'pale')},
    'pale_blue_to_gold_trim': {'rgb': (170, 190, 215), 'expected': ((248, 228, 168), 'trim')},
    'saturated_blue_to_purple_robe': {'rgb': (40, 70, 160), 'expected': ((107, 37, 138), 'robe')},
    'teal_to_amber': {'rgb': (40, 150, 150), 'expected': ((226, 152, 25), 'amber')},
}


def _rgba(pixels: list[tuple[int, int, int, int]]) -> Image.Image:
    """Build a one-row RGBA image from pixels."""
    image = Image.new('RGBA', (len(pixels), 1))
    image.putdata(pixels)
    return image


@pytest.mark.parametrize(
    'rgb, rules, expected',
    [(case['rgb'], case['rules'], case['expected']) for case in _match_rule_cases.values()],
    ids=list(_match_rule_cases.keys()),
)
def test_match_rule(rgb: Rgb, rules: tuple[Rule, ...], expected: str | None) -> None:
    """Test match_rule returns the first matching rule's name, or None."""
    rule = match_rule(rgb, rules)

    assert (rule.name if rule else None) == expected


@pytest.mark.parametrize(
    'rule, hls, expected',
    [(case['rule'], case['hls'], case['expected']) for case in _matches_cases.values()],
    ids=list(_matches_cases.keys()),
)
def test_matches(rule: Rule, hls: tuple[float, float, float], expected: bool) -> None:
    """Test Rule.matches treats every range as inclusive at both ends."""
    assert rule.matches(*hls) is expected


@pytest.mark.parametrize(
    'rgb, expected',
    [(case['rgb'], case['expected']) for case in _recolour_rgb_cases.values()],
    ids=list(_recolour_rgb_cases.keys()),
)
def test_recolour_rgb(rgb: Rgb, expected: tuple[Rgb, str | None]) -> None:
    """Test recolour_rgb keeps shading, applies the first matching rule, and leaves others alone."""
    assert recolour_rgb(rgb, _RULES) == expected


def test_recolour_image_converts_non_palette_images_to_rgba() -> None:
    """Test an RGB texture comes back as RGBA with its colours recoloured."""
    image = Image.new('RGB', (1, 1), (40, 70, 160))

    result, counts = recolour_image(image, _RULES)

    assert result.mode == 'RGBA'
    assert result.getpixel((0, 0)) == (107, 37, 138, 255)
    assert counts == {'robe': 1}


def test_recolour_image_edits_palette_in_place() -> None:
    """Test a palette texture keeps its mode, size, pixel indices and transparency."""
    with Image.open(FIXTURE_PATH) as vanilla:
        vanilla.load()

    result, counts = recolour_image(vanilla, _RULES)

    assert (result.mode, result.size) == (vanilla.mode, vanilla.size)
    assert result.info['transparency'] == vanilla.info['transparency']
    assert list(result.get_flattened_data()) == list(vanilla.get_flattened_data())
    assert result.getpalette()[3:6] == [107, 37, 138]
    assert counts == {'amber': 1, 'pale': 1, 'robe': 1, 'trim': 1}


def test_recolour_image_skips_transparent_palette_entry() -> None:
    """Test the palette's transparent entry is never recoloured, even when it matches a rule."""
    image = Image.new('P', (2, 1))
    image.putpalette([40, 70, 160, 40, 70, 160])
    image.info['transparency'] = 0

    result, counts = recolour_image(image, _RULES)

    assert result.getpalette()[:6] == [40, 70, 160, 107, 37, 138]
    assert counts == {'robe': 1}


def test_recolour_image_skips_transparent_pixels_and_keeps_alpha() -> None:
    """Test fully transparent pixels are left alone and partial alpha is preserved."""
    image = _rgba([(40, 70, 160, 0), (40, 70, 160, 128), (150, 150, 150, 255)])

    result, counts = recolour_image(image, _RULES)

    assert list(result.get_flattened_data()) == [(40, 70, 160, 0), (107, 37, 138, 128), (150, 150, 150, 255)]
    assert counts == {'robe': 1}
