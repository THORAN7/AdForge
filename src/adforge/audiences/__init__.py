"""Audience registry and adaptation public API."""

from .adapter import build_creative_brief, profile_for
from .constants import PRESET_IDS
from .registry import list_profiles, load_profile

__all__ = [
    "PRESET_IDS",
    "build_creative_brief",
    "list_profiles",
    "load_profile",
    "profile_for",
]
