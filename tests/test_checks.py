from adforge.checks import review_package
from adforge.generation import TemplateProvider
from adforge.models import AudienceSelection, ProductInput


def test_generated_package_passes_core_checks() -> None:
    product = ProductInput(
        name="Lamp",
        category="lighting",
        key_features=["adjustable", "portable", "USB-C"],
        price_offer="$20",
        unique_selling_point="Focused light.",
        brand_name="Brand",
        brand_tone="trustworthy",
    )
    package = TemplateProvider().generate(
        product, AudienceSelection(preset="young_professionals")
    )
    assert package.consistency_warnings == []
    assert package.compliance_warnings == []
    assert package.quality_score == 100


def test_claim_checker_flags_seeded_violation() -> None:
    product = ProductInput(
        name="Lamp",
        category="lighting",
        key_features=["adjustable", "portable", "USB-C"],
        unique_selling_point="Focused light.",
        brand_name="Brand",
        brand_tone="trustworthy",
    )
    package = TemplateProvider().generate(
        product, AudienceSelection(preset="young_professionals")
    )
    package.product_descriptions.one_liner = "The best lamp."
    reviewed = review_package(package)
    assert reviewed.compliance_warnings
    assert reviewed.quality_score < 100
