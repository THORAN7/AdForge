"""Cross-section fact consistency checks."""

from adforge.models import AdPackage


def check_consistency(package: AdPackage) -> list[str]:
    """Ensure the product name and offer remain visible across core sections."""
    warnings: list[str] = []
    name = package.product.name
    offer = package.product.price_offer
    sections = [
        package.product_descriptions.model_dump(),
        package.promotional_text.model_dump(),
        package.social_media.model_dump(),
        package.visual_concepts.model_dump(),
        package.video_narration.model_dump(),
    ]
    for section in sections:
        text = str(section)
        if name not in text:
            warnings.append(f"product name missing from section: {name}")
        if offer and offer not in text:
            warnings.append(f"offer missing from section: {offer}")
    return warnings
