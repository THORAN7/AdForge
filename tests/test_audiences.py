from adforge.audiences import build_creative_brief, load_profile
from adforge.models import AudienceSelection, ProductInput


def product() -> ProductInput:
    return ProductInput(
        name="Focus Lamp",
        category="desk lighting",
        key_features=["adjustable", "portable", "USB-C"],
        unique_selling_point="Focused light for flexible workspaces.",
        brand_name="Northstar",
        brand_tone="trustworthy",
    )


def test_profiles_are_loaded_from_registry() -> None:
    profile = load_profile(AudienceSelection(preset="gen_z_students"))
    assert profile.name == "Gen Z students"
    assert "TikTok" in profile.platform_mix


def test_audiences_produce_substantively_different_briefs() -> None:
    student = build_creative_brief(
        product(), AudienceSelection(preset="gen_z_students")
    )
    luxury = build_creative_brief(product(), AudienceSelection(preset="luxury_buyers"))
    assert student.channel_emphasis != luxury.channel_emphasis
    assert student.tone != luxury.tone
    assert student.imagery_style != luxury.imagery_style


def test_custom_audience_uses_same_profile_contract() -> None:
    selection = AudienceSelection(
        custom={
            "age_range": "25-40",
            "interests": ["home office"],
            "values": ["simplicity"],
            "pain_points": ["clutter"],
            "preferred_platforms": ["LinkedIn"],
        }
    )
    profile = load_profile(selection)
    brief = build_creative_brief(product(), selection)
    assert profile.id == "custom"
    assert brief.audience_profile_id == "custom"
