from adforge.generation import TemplateProvider
from adforge.models import AudienceSelection, ProductInput


def test_template_provider_is_offline_and_grounded() -> None:
    product = ProductInput(
        name="Focus Lamp",
        category="desk lighting",
        key_features=["adjustable", "portable", "USB-C"],
        price_offer="$19.99",
        unique_selling_point="Focused light for flexible workspaces.",
        brand_name="Northstar",
        brand_tone="trustworthy",
    )
    package = TemplateProvider().generate(
        product, AudienceSelection(preset="young_professionals")
    )
    assert package.quality_score == 100
    assert "Focus Lamp" in package.claims_ledger
    assert package.product.offer is not None
    assert package.promotional_text.google_ads.headlines


def test_template_provider_adapts_channel_and_brief() -> None:
    product = ProductInput(
        name="Focus Lamp",
        category="desk lighting",
        key_features=["adjustable", "portable", "USB-C"],
        unique_selling_point="Focused light for flexible workspaces.",
        brand_name="Northstar",
        brand_tone="trustworthy",
    )
    student = TemplateProvider().generate(
        product, AudienceSelection(preset="gen_z_students")
    )
    luxury = TemplateProvider().generate(
        product, AudienceSelection(preset="luxury_buyers")
    )
    assert (
        student.creative_brief.channel_emphasis
        != luxury.creative_brief.channel_emphasis
    )
    assert student.visual_concepts.art_direction != luxury.visual_concepts.art_direction
