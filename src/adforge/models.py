"""Canonical typed boundaries for AdForge inputs and generated packages."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

BrandTone = Literal["playful", "premium", "trustworthy", "bold"]
CampaignGoal = Literal["awareness", "conversion", "launch", "seasonal_sale"]


class CustomAudience(BaseModel):
    """User-defined audience characteristics."""

    age_range: str = Field(min_length=1, max_length=80)
    interests: list[str] = Field(min_length=1, max_length=20)
    values: list[str] = Field(default_factory=list, max_length=20)
    pain_points: list[str] = Field(default_factory=list, max_length=20)
    preferred_platforms: list[str] = Field(default_factory=list, max_length=10)
    budget_sensitivity: Literal["low", "medium", "high"] = "medium"


class AudienceSelection(BaseModel):
    """Either a documented preset or a custom audience."""

    preset: str | None = Field(default=None, min_length=1, max_length=80)
    custom: CustomAudience | None = None


class ProductInput(BaseModel):
    """Facts supplied by a user; downstream generation must remain grounded here."""

    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=120)
    category: str = Field(min_length=1, max_length=80)
    key_features: Annotated[list[str], Field(min_length=3, max_length=8)]
    price_offer: str | None = Field(default=None, max_length=160)
    unique_selling_point: str = Field(min_length=1, max_length=500)
    brand_name: str = Field(min_length=1, max_length=120)
    brand_tone: BrandTone
    brand_colors: list[str] = Field(default_factory=list, max_length=8)
    logo_text: str | None = Field(default=None, max_length=120)
    campaign_goal: CampaignGoal | None = None
    language: str = Field(default="English", min_length=2, max_length=40)


class GenerateRequest(BaseModel):
    """Initial API request model, intentionally separate from generated output."""

    product: ProductInput
    audiences: Annotated[list[AudienceSelection], Field(min_length=1, max_length=3)]


class AdPackage(BaseModel):
    """Canonical output envelope shared by all exporters and API responses."""

    model_config = ConfigDict(extra="forbid")

    product: ProductInput
    audience: AudienceSelection
    product_descriptions: dict[str, object] = Field(default_factory=dict)
    promotional_text: dict[str, object] = Field(default_factory=dict)
    social_media: dict[str, object] = Field(default_factory=dict)
    visual_concepts: dict[str, object] = Field(default_factory=dict)
    video_narration: dict[str, object] = Field(default_factory=dict)
    compliance_warnings: list[str] = Field(default_factory=list)
    quality_score: float | None = Field(default=None, ge=0, le=100)

