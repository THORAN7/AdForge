from adforge.generation import TemplateProvider
from adforge.models import AudienceSelection, ProductInput
from adforge.visuals import LocalImageProvider, render_preview_cards


def test_local_visual_previews_are_svg() -> None:
    cards = render_preview_cards("Lamp", ["Show the lamp"], ["#112233"])
    assert len(cards) == 2
    assert cards[0].startswith("<svg")
    assert "Lamp" in cards[0]


def test_image_provider_is_offline_by_default() -> None:
    assert LocalImageProvider().render("prompt") == b""


def test_generated_package_contains_visual_previews() -> None:
    product = ProductInput(
        name="Lamp",
        category="lighting",
        key_features=["adjustable", "portable", "USB-C"],
        unique_selling_point="Focused light.",
        brand_name="Brand",
        brand_tone="trustworthy",
    )
    package = TemplateProvider().generate(
        product, AudienceSelection(preset="tech_early_adopters")
    )
    assert len(package.visual_concepts.svg_previews) == 7
