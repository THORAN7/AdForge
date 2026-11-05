"""Audience profile loading and custom-audience normalization."""

import json
from pathlib import Path

from adforge.models import AudienceProfile, AudienceSelection

DATA_DIR = Path(__file__).resolve().parents[3] / "data" / "audiences"


def _profile_path(profile_id: str) -> Path:
    return DATA_DIR / f"{profile_id}.json"


def load_profile(selection: AudienceSelection) -> AudienceProfile:
    """Load a preset profile or normalize a custom selection."""
    if selection.preset:
        path = _profile_path(selection.preset)
        if not path.is_file():
            raise ValueError(f"audience profile is missing: {selection.preset}")
        return AudienceProfile.model_validate(
            json.loads(path.read_text(encoding="utf-8"))
        )
    if selection.custom is None:
        raise ValueError("audience selection has no profile")
    custom = selection.custom
    return AudienceProfile(
        id="custom",
        name=f"Custom audience ({custom.age_range})",
        tone="clear and inclusive",
        vocabulary=custom.interests + custom.values,
        flesch_target_min=55,
        flesch_target_max=75,
        sentence_length="short to medium",
        emoji_density="low",
        slang_density="low",
        emotional_triggers=custom.values,
        objections=custom.pain_points,
        benefit_priority=custom.interests,
        platform_mix=custom.preferred_platforms,
        imagery_style="inclusive, authentic product-in-use imagery",
        cta_style="clear and specific",
        humor_level="light",
    )


def list_profiles() -> list[AudienceProfile]:
    """Return all documented preset profiles in stable order."""
    return [
        AudienceProfile.model_validate(json.loads(path.read_text(encoding="utf-8")))
        for path in sorted(DATA_DIR.glob("*.json"))
    ]
