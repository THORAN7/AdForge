"""Canonical typed boundaries for AdForge inputs and generated packages."""

import re
from datetime import datetime
from decimal import Decimal
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from adforge.audiences.constants import PRESET_IDS

BrandTone = Literal["playful", "premium", "trustworthy", "bold"]
CampaignGoal = Literal["awareness", "conversion", "launch", "seasonal_sale"]
StringItem = Annotated[str, Field(min_length=1, max_length=160)]
HexColor = Annotated[str, Field(pattern=r"^#[0-9A-Fa-f]{6}$")]
_LANGUAGE_PATTERN = re.compile(r"^[A-Za-z]{2,40}(?:[-_][A-Za-z]{2,8})?$")
_MONEY_PATTERN = re.compile(
    r"(?P<currency>[$€£]|[A-Z]{3})?\s*(?P<amount>\d+(?:[.,]\d{1,2})?)"
)


class Offer(BaseModel):
    """Structured offer data derived from the user-supplied raw text."""

    model_config = ConfigDict(extra="forbid")

    raw_text: str = Field(min_length=1, max_length=160)
    amount: Decimal | None = None
    currency: str | None = Field(default=None, min_length=1, max_length=3)
    discount_percent: Decimal | None = Field(default=None, ge=0, le=100)
    valid_until: datetime | None = None

    @classmethod
    def from_raw_text(cls, raw_text: str) -> "Offer":
        """Parse conservative price information without inventing missing facts."""
        match = _MONEY_PATTERN.search(raw_text)
        amount: Decimal | None = None
        currency: str | None = None
        if match:
            amount = Decimal(match.group("amount").replace(",", "."))
            currency = match.group("currency")
            if currency in {"$", "€", "£"}:
                currency = {"$": "USD", "€": "EUR", "£": "GBP"}[currency]
        discount_match = re.search(r"(\d{1,3}(?:\.\d+)?)\s*%\s*off", raw_text, re.I)
        discount = Decimal(discount_match.group(1)) if discount_match else None
        return cls(
            raw_text=raw_text,
            amount=amount,
            currency=currency,
            discount_percent=discount,
        )


class CustomAudience(BaseModel):
    """User-defined audience characteristics."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    age_range: str = Field(min_length=1, max_length=80)
    interests: list[StringItem] = Field(min_length=1, max_length=20)
    values: list[StringItem] = Field(default_factory=list, max_length=20)
    pain_points: list[StringItem] = Field(default_factory=list, max_length=20)
    preferred_platforms: list[StringItem] = Field(default_factory=list, max_length=10)
    budget_sensitivity: Literal["low", "medium", "high"] = "medium"


class AudienceProfile(BaseModel):
    """Normalized audience strategy used by the adaptation engine."""

    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    tone: str
    vocabulary: list[StringItem] = Field(default_factory=list, max_length=20)
    flesch_target_min: float = Field(ge=0, le=100)
    flesch_target_max: float = Field(ge=0, le=100)
    sentence_length: str
    emoji_density: str
    slang_density: str
    emotional_triggers: list[StringItem] = Field(default_factory=list, max_length=10)
    objections: list[StringItem] = Field(default_factory=list, max_length=10)
    benefit_priority: list[StringItem] = Field(default_factory=list, max_length=10)
    platform_mix: list[StringItem] = Field(default_factory=list, max_length=10)
    imagery_style: str
    cta_style: str
    humor_level: str


class AudienceSelection(BaseModel):
    """Either a documented preset or a custom audience."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    preset: str | None = Field(default=None, min_length=1, max_length=80)
    custom: CustomAudience | None = None

    @model_validator(mode="after")
    def validate_exactly_one_audience(self) -> "AudienceSelection":
        """Require one, and only one, audience source."""
        if (self.preset is None) == (self.custom is None):
            raise ValueError("exactly one of preset or custom must be provided")
        if self.preset is not None and self.preset not in PRESET_IDS:
            raise ValueError(f"unknown audience preset: {self.preset}")
        return self


class ProductInput(BaseModel):
    """Facts supplied by a user; downstream generation must remain grounded here."""

    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=120)
    category: str = Field(min_length=1, max_length=80)
    key_features: Annotated[list[StringItem], Field(min_length=3, max_length=8)]
    price_offer: str | None = Field(default=None, max_length=160)
    unique_selling_point: str = Field(min_length=1, max_length=500)
    brand_name: str = Field(min_length=1, max_length=120)
    brand_tone: BrandTone
    brand_colors: list[HexColor] = Field(default_factory=list, max_length=8)
    logo_text: str | None = Field(default=None, max_length=120)
    campaign_goal: CampaignGoal | None = None
    language: str = Field(default="English", min_length=2, max_length=40)
    offer: Offer | None = None

    @model_validator(mode="after")
    def validate_language_and_offer(self) -> "ProductInput":
        """Validate language tags and derive structured offer data."""
        if not _LANGUAGE_PATTERN.fullmatch(self.language):
            raise ValueError("language must be a language name or BCP-47-like tag")
        if self.price_offer:
            self.offer = Offer.from_raw_text(self.price_offer)
        elif self.offer is not None:
            raise ValueError("offer requires price_offer")
        return self


class CreativeBrief(BaseModel):
    """Shared creative direction consumed by every future writer."""

    model_config = ConfigDict(extra="forbid")

    message_pillars: list[StringItem] = Field(default_factory=list, max_length=8)
    lead_benefit: str | None = Field(default=None, max_length=300)
    proof_points: list[StringItem] = Field(default_factory=list, max_length=8)
    tone: str | None = Field(default=None, max_length=80)
    cta: str | None = Field(default=None, max_length=120)
    channel_emphasis: list[StringItem] = Field(default_factory=list, max_length=10)
    audience_profile_id: str | None = Field(default=None, max_length=80)
    reading_level_target: str | None = Field(default=None, max_length=80)
    imagery_style: str | None = Field(default=None, max_length=160)
    humor_level: str | None = Field(default=None, max_length=40)


class ProductDescriptions(BaseModel):
    """Typed product description assets."""

    model_config = ConfigDict(extra="forbid")

    one_liner: str = ""
    short: str = ""
    long: str = ""
    seo_title: str = ""
    seo_meta_description: str = ""
    feature_bullets: list[StringItem] = Field(default_factory=list, max_length=8)


class AdCopyVariant(BaseModel):
    """One promotional copy angle."""

    angle: Literal["benefit", "emotion", "urgency"]
    text: str = ""


class GoogleAdsSet(BaseModel):
    """Google Ads assets with bounded fields."""

    headlines: list[Annotated[str, Field(max_length=30)]] = Field(
        default_factory=list, max_length=15
    )
    descriptions: list[Annotated[str, Field(max_length=90)]] = Field(
        default_factory=list, max_length=4
    )


class PromotionalText(BaseModel):
    """Typed promotional assets."""

    model_config = ConfigDict(extra="forbid")

    headlines: list[StringItem] = Field(default_factory=list, max_length=5)
    taglines: list[StringItem] = Field(default_factory=list, max_length=3)
    ad_copy_variants: list[AdCopyVariant] = Field(default_factory=list, max_length=3)
    ctas: list[StringItem] = Field(default_factory=list, max_length=8)
    email_subject_lines: list[StringItem] = Field(default_factory=list, max_length=8)
    email_preheaders: list[StringItem] = Field(default_factory=list, max_length=8)
    google_ads: GoogleAdsSet = Field(default_factory=GoogleAdsSet)


class InstagramContent(BaseModel):
    caption: str = ""
    hashtags: list[Annotated[str, Field(max_length=60)]] = Field(
        default_factory=list, max_length=30
    )
    alt_text: str = ""


class FacebookContent(BaseModel):
    post: str = ""


class XContent(BaseModel):
    post: Annotated[str, Field(max_length=280)] = ""
    thread: list[Annotated[str, Field(max_length=280)]] = Field(
        default_factory=list, max_length=10
    )


class LinkedInContent(BaseModel):
    post: str = ""


class TikTokContent(BaseModel):
    hook: str = ""
    caption: str = ""


class CalendarPost(BaseModel):
    day: int = Field(ge=1, le=7)
    post_type: str = ""
    timing: str = ""
    goal: str = ""


class SocialMediaContent(BaseModel):
    """Typed platform-specific social content."""

    model_config = ConfigDict(extra="forbid")

    instagram: InstagramContent = Field(default_factory=InstagramContent)
    facebook: FacebookContent = Field(default_factory=FacebookContent)
    x: XContent = Field(default_factory=XContent)
    linkedin: LinkedInContent = Field(default_factory=LinkedInContent)
    tiktok_reels: TikTokContent = Field(default_factory=TikTokContent)
    calendar: list[CalendarPost] = Field(default_factory=list, max_length=7)


class VisualConcepts(BaseModel):
    """Typed visual direction boundary."""

    model_config = ConfigDict(extra="forbid")

    art_direction: str = ""
    color_palette: list[HexColor] = Field(default_factory=list, max_length=8)
    typography: list[StringItem] = Field(default_factory=list, max_length=8)
    hero_concepts: list[StringItem] = Field(default_factory=list, max_length=3)
    poster_layout: str = ""
    storyboard: list[StringItem] = Field(default_factory=list, max_length=8)
    svg_previews: list[str] = Field(default_factory=list, max_length=9)


class VideoScene(BaseModel):
    timestamp: str = ""
    visual: str = ""
    voiceover: str = ""
    on_screen_text: str = ""
    music_sfx: str = ""


class VideoNarration(BaseModel):
    """Typed video and TTS assets."""

    model_config = ConfigDict(extra="forbid")

    script_15s: list[VideoScene] = Field(default_factory=list, max_length=8)
    script_30s: list[VideoScene] = Field(default_factory=list, max_length=8)
    script_60s: list[VideoScene] = Field(default_factory=list, max_length=8)
    ssml: str = ""


class GenerateRequest(BaseModel):
    """Initial API request model, intentionally separate from generated output."""

    product: ProductInput
    audiences: Annotated[list[AudienceSelection], Field(min_length=1, max_length=3)]


class AdPackage(BaseModel):
    """Canonical output envelope shared by all exporters and API responses."""

    model_config = ConfigDict(extra="forbid")

    schema_version: str = "1.0"
    generated_at: datetime | None = None
    product: ProductInput
    audience: AudienceSelection
    creative_brief: CreativeBrief = Field(default_factory=CreativeBrief)
    claims_ledger: list[StringItem] = Field(default_factory=list, max_length=100)
    product_descriptions: ProductDescriptions = Field(
        default_factory=ProductDescriptions
    )
    promotional_text: PromotionalText = Field(default_factory=PromotionalText)
    social_media: SocialMediaContent = Field(default_factory=SocialMediaContent)
    visual_concepts: VisualConcepts = Field(default_factory=VisualConcepts)
    video_narration: VideoNarration = Field(default_factory=VideoNarration)
    compliance_warnings: list[str] = Field(default_factory=list)
    consistency_warnings: list[str] = Field(default_factory=list)
    quality_score: float | None = Field(default=None, ge=0, le=100)
