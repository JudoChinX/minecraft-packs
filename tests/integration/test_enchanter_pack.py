"""Tests pinning the shipped enchanter pack: its sources, and the recolour it applies.

The vanilla texture is never available to the tests, so the recolour is pinned against the
synthetic fixture's palette. A change here changes the pack's look and its SHA-1.
"""

import pytest
from PIL import Image

from minecraft_packs.config import load_pack
from minecraft_packs.models import MODELS
from minecraft_packs.recolour import recolour_image
from tests.helpers import FIXTURE_PATH
from tests.helpers import REPO_ROOT

_ENCHANTER = load_pack(REPO_ROOT / 'packs' / 'enchanter')

_palette_cases = {
    'blue_violet_to_pale_gold': {'index': 4, 'expected': [242, 231, 161]},
    'dark_shirt_untouched': {'index': 6, 'expected': [50, 50, 60]},
    'green_eyes_untouched': {'index': 7, 'expected': [60, 160, 60]},
    'grey_skin_untouched': {'index': 5, 'expected': [150, 150, 150]},
    'pale_blue_to_gold_trim': {'index': 2, 'expected': [248, 228, 168]},
    'saturated_blue_to_purple_robe': {'index': 1, 'expected': [107, 37, 138]},
    'teal_to_amber': {'index': 3, 'expected': [226, 152, 25]},
    'transparent_untouched': {'index': 0, 'expected': [0, 0, 0]},
}


@pytest.mark.parametrize(
    'index, expected',
    [(case['index'], case['expected']) for case in _palette_cases.values()],
    ids=list(_palette_cases.keys()),
)
def test_enchanter_recolour(index: int, expected: list[int]) -> None:
    """Test the enchanter's rules turn each fixture colour into the reviewed result."""
    with Image.open(FIXTURE_PATH) as vanilla:
        vanilla.load()

    result, _ = recolour_image(vanilla, _ENCHANTER.textures[0].rules)

    assert result.getpalette()[index * 3 : index * 3 + 3] == expected


def test_enchanter_sources() -> None:
    """Test the enchanter pins Minecraft 26.3's client jar and Illusioner texture, and targets format 97."""
    texture = _ENCHANTER.textures[0]

    assert _ENCHANTER.vanilla is not None
    assert (_ENCHANTER.vanilla.version, _ENCHANTER.vanilla.client_sha1) == (
        '26.3',
        'e877b6a07acd633fb3bb475002175cec036e7b87',
    )
    assert texture.path == 'assets/minecraft/textures/entity/illager/illusioner.png'
    assert texture.sha256 == 'f43b9eecec0f7c846f673297c5ceff16b091359c589b8646abf82c5308bbfa75'
    assert [rule.name for rule in texture.rules] == ['robe', 'trim', 'amber', 'pale']
    assert (_ENCHANTER.min_format, _ENCHANTER.max_format) == (97, 97)
    assert _ENCHANTER.preview is not None and _ENCHANTER.preview.model in MODELS
