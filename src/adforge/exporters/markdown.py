"""Human-readable Markdown export."""

from adforge.models import AdPackage


def to_markdown(package: AdPackage) -> bytes:
    """Render the canonical package as Markdown."""
    product = package.product
    descriptions = package.product_descriptions
    promo = package.promotional_text
    social = package.social_media
    lines = [
        f"# {product.name}",
        "",
        f"**Brand:** {product.brand_name}  ",
        f"**Offer:** {product.price_offer or 'Not supplied'}  ",
        f"**USP:** {product.unique_selling_point}",
        "",
        "## Descriptions",
        f"**One-liner:** {descriptions.one_liner}",
        "",
        descriptions.short,
        "",
        descriptions.long,
        "",
        "### Features",
        *[f"- {item}" for item in descriptions.feature_bullets],
        "",
        "## Promotion",
        "### Headlines",
        *[f"- {item}" for item in promo.headlines],
        "",
        "### Ad copy",
        *[f"- {item.text}" for item in promo.ad_copy_variants],
        "",
        "## Social",
        f"**Instagram:** {social.instagram.caption}",
        "",
        f"**Facebook:** {social.facebook.post}",
        "",
        f"**X:** {social.x.post}",
        "",
        "## Visual direction",
        package.visual_concepts.art_direction,
        "",
        "## Video narration",
        package.video_narration.ssml,
        "",
        "## Review",
        f"Quality score: {package.quality_score}",
    ]
    return "\n".join(lines).encode("utf-8")
