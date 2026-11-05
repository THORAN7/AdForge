"""Audience adaptation from product facts to a shared creative brief."""

from adforge.models import (
    AudienceProfile,
    AudienceSelection,
    CreativeBrief,
    ProductInput,
)

from .registry import load_profile


def build_creative_brief(
    product: ProductInput, selection: AudienceSelection
) -> CreativeBrief:
    """Prioritize supplied benefits and proof points for one audience."""
    profile = load_profile(selection)
    features = list(product.key_features)
    priorities = profile.benefit_priority
    prioritized = [
        feature
        for keyword in priorities
        for feature in features
        if keyword.lower() in feature.lower()
    ]
    ordered_features = list(dict.fromkeys(prioritized + features))
    lead = ordered_features[0] if ordered_features else product.unique_selling_point
    cta = {
        "action-oriented": "Try it today",
        "value-focused": "See the value",
        "reassuring": "Learn more",
        "premium": "Explore the collection",
    }.get(profile.cta_style, "Learn more")
    tone = f"{product.brand_tone}, {profile.tone}"
    return CreativeBrief(
        audience_profile_id=profile.id,
        message_pillars=[product.unique_selling_point, *ordered_features[:3]],
        lead_benefit=lead,
        proof_points=ordered_features[:4],
        tone=tone,
        cta=cta,
        channel_emphasis=profile.platform_mix[:4],
        reading_level_target=(
            f"Flesch {profile.flesch_target_min:.0f}-{profile.flesch_target_max:.0f}"
        ),
        imagery_style=profile.imagery_style,
        humor_level=profile.humor_level,
    )


def profile_for(selection: AudienceSelection) -> AudienceProfile:
    """Expose the normalized profile for callers and future checkers."""
    return load_profile(selection)
