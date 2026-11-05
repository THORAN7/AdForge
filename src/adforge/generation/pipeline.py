"""Offline staged package generation from grounded product facts."""

from datetime import UTC, datetime

from adforge.audiences import build_creative_brief, profile_for
from adforge.checks import review_package
from adforge.models import (
    AdCopyVariant,
    AdPackage,
    AudienceSelection,
    CalendarPost,
    CreativeBrief,
    FacebookContent,
    GoogleAdsSet,
    InstagramContent,
    LinkedInContent,
    ProductDescriptions,
    ProductInput,
    PromotionalText,
    SocialMediaContent,
    TikTokContent,
    VideoNarration,
    VideoScene,
    VisualConcepts,
    XContent,
)
from adforge.visuals import render_preview_cards


def _offer_line(product: ProductInput) -> str:
    return product.price_offer or "Offer details available from the brand."


def _claims(product: ProductInput) -> list[str]:
    claims = [product.name, product.category, product.unique_selling_point]
    claims.extend(product.key_features)
    if product.price_offer:
        claims.append(product.price_offer)
    return claims


def _descriptions(product: ProductInput, brief: CreativeBrief) -> ProductDescriptions:
    facts = ", ".join(product.key_features)
    lead = brief.lead_benefit or product.unique_selling_point
    short = (
        f"{product.name} is {product.unique_selling_point} "
        f"Built around {facts}, it brings {lead.lower()} "
        f"to your everyday routine. {_offer_line(product)}"
    )
    long = (
        f"Meet {product.name} from {product.brand_name}, a {product.category} "
        f"created for people who value {lead.lower()}. "
        f"{product.unique_selling_point} "
        f"Key features include {facts}. "
        f"The {product.brand_tone} brand voice keeps the message clear and grounded "
        f"in the details supplied for this campaign. {_offer_line(product)} "
        f"Choose the features that fit your routine and "
        f"{(brief.cta or 'learn more').lower()}."
    )
    return ProductDescriptions(
        one_liner=f"{product.name}: {brief.lead_benefit}.",
        short=short,
        long=long,
        seo_title=f"{product.name} | {product.brand_name}",
        seo_meta_description=f"{product.name}: {product.unique_selling_point}",
        feature_bullets=[f"{feature}" for feature in product.key_features],
    )


def _promotion(product: ProductInput, brief: CreativeBrief) -> PromotionalText:
    lead = brief.lead_benefit or product.unique_selling_point
    cta = brief.cta or "Learn more"
    headlines = [
        f"{product.name}: {lead}",
        f"Make room for {product.name}",
        f"{product.name}, made clear",
        f"Built around {product.name}",
        f"{cta}: {product.name}",
    ]
    return PromotionalText(
        headlines=headlines,
        taglines=[lead, product.unique_selling_point, f"{cta} with confidence."],
        ad_copy_variants=[
            AdCopyVariant(
                angle="benefit",
                text=f"{product.name} puts {lead.lower()} into focus. {cta}.",
            ),
            AdCopyVariant(
                angle="emotion",
                text=(
                    f"Feel good about choosing {product.name}: "
                    f"{product.unique_selling_point}"
                ),
            ),
            AdCopyVariant(
                angle="urgency",
                text=f"Ready for a clearer next step? Explore {product.name} today.",
            ),
        ],
        ctas=[cta, "Explore the details", "See how it fits"],
        email_subject_lines=[
            f"Meet {product.name}",
            f"A clearer way to {lead.lower()}",
            f"{product.name}: details worth exploring",
        ],
        email_preheaders=[
            product.unique_selling_point,
            f"See the features behind {product.name}.",
            _offer_line(product),
        ],
        google_ads=GoogleAdsSet(
            headlines=[
                item[:30]
                for item in [
                    product.name,
                    f"{lead}",
                    f"Explore {product.name}",
                    f"{cta} today",
                ]
            ],
            descriptions=[
                f"{product.name}: {product.unique_selling_point}"[:90],
                f"Explore the features. {_offer_line(product)}"[:90],
            ],
        ),
    )


def _social(
    product: ProductInput, brief: CreativeBrief, profile_name: str
) -> SocialMediaContent:
    lead = brief.lead_benefit or product.unique_selling_point
    caption = (
        f"{product.name} is built for {lead.lower()}. "
        f"{product.unique_selling_point} {_offer_line(product)} #ad"
    )
    calendar = [
        CalendarPost(
            day=day,
            post_type=post_type,
            timing="12:00 local time",
            goal=goal,
        )
        for day, post_type, goal in [
            (1, "hero post", "awareness"),
            (2, "feature detail", "education"),
            (3, "audience use case", "relevance"),
            (4, "FAQ", "trust"),
            (5, "behind the message", "engagement"),
            (6, "offer reminder", "conversion"),
            (7, "summary", "conversion"),
        ]
    ]
    return SocialMediaContent(
        instagram=InstagramContent(
            caption=caption,
            hashtags=["#AdForge", "#ad", f"#{product.category.replace(' ', '')}"],
            alt_text=(
                f"{product.name}, a {product.category}, shown in an everyday setting."
            ),
        ),
        facebook=FacebookContent(
            post=f"{product.name}: {product.unique_selling_point} "
            f"Explore the details and see whether it fits your routine. #ad"
        ),
        x=XContent(
            post=f"{product.name}: {lead}. {brief.cta or 'Learn more'}. #ad"[:280],
            thread=[
                f"1/ {product.unique_selling_point}",
                f"2/ Features: {', '.join(product.key_features)}",
                f"3/ {brief.cta or 'Learn more'}",
            ],
        ),
        linkedin=LinkedInContent(
            post=f"{product.name} supports {lead.lower()} with a focused set of "
            f"features: {', '.join(product.key_features)}. #ad"
        ),
        tiktok_reels=TikTokContent(
            hook=f"Looking for {lead.lower()}?",
            caption=f"{product.name}: {product.unique_selling_point} #ad",
        ),
        calendar=calendar,
    )


def _visuals(product: ProductInput, brief: CreativeBrief) -> VisualConcepts:
    palette = product.brand_colors or ["#0B1020", "#7DD3FC", "#E7EEFB"]
    storyboard = [
        f"Frame {number}: show {product.name} and supplied product facts."
        for number in range(1, 7)
    ]
    return VisualConcepts(
        art_direction=(
            f"{brief.imagery_style or 'clean product-in-use imagery'}; "
            f"{product.brand_tone} mood; clear product focus. {_offer_line(product)}"
        ),
        color_palette=palette,
        typography=["Readable sans-serif headline", "Accessible body text"],
        hero_concepts=[
            f"{product.name} in a real {product.category} setting",
            f"Close detail of {product.name} highlighting {brief.lead_benefit}",
            f"Audience-relevant moment featuring {product.name}",
        ],
        poster_layout=(
            f"Headline at top; {product.name} centered; "
            f"CTA '{brief.cta}' at bottom. {_offer_line(product)}"
        ),
        storyboard=storyboard,
        svg_previews=render_preview_cards(product.name, storyboard, palette),
    )


def _video(product: ProductInput, brief: CreativeBrief) -> VideoNarration:
    voice = f"{product.name}: {product.unique_selling_point}"
    scenes = [
        VideoScene(
            timestamp="0-3s",
            visual=f"Introduce {product.name}",
            voiceover=f"{voice} {_offer_line(product)}",
            on_screen_text=product.name,
            music_sfx="Light, clear opening",
        ),
        VideoScene(
            timestamp="3-10s",
            visual="Show supplied features in use",
            voiceover=f"Explore {', '.join(product.key_features[:3])}.",
            on_screen_text=", ".join(product.key_features[:3]),
            music_sfx="Gentle transition",
        ),
        VideoScene(
            timestamp="10-15s",
            visual="Close on product and CTA",
            voiceover=f"{brief.cta or 'Learn more'} about {product.name}.",
            on_screen_text=brief.cta or "Learn more",
            music_sfx="Clean resolve",
        ),
    ]
    ssml = (
        "<speak><p>"
        f"{voice} "
        f"Explore {', '.join(product.key_features[:3])}. "
        f"{brief.cta or 'Learn more'} about {product.name}."
        "</p></speak>"
    )
    context_scene = VideoScene(
        timestamp="15-30s",
        visual="Show audience context",
        voiceover=f"{brief.lead_benefit}.",
        on_screen_text=brief.lead_benefit or "",
        music_sfx="Warm lift",
    )
    close_scene = VideoScene(
        timestamp="30-60s",
        visual="Summarize supplied facts and offer",
        voiceover=f"{_offer_line(product)} {brief.cta or 'Learn more'}.",
        on_screen_text=_offer_line(product),
        music_sfx="Confident close",
    )
    return VideoNarration(
        script_15s=scenes,
        script_30s=[*scenes, context_scene],
        script_60s=[*scenes, context_scene, close_scene],
        ssml=ssml,
    )


def generate_package(product: ProductInput, audience: AudienceSelection) -> AdPackage:
    """Run the deterministic analyzer, adapter, writers, and reviewer."""
    profile = profile_for(audience)
    brief = build_creative_brief(product, audience)
    package = AdPackage(
        schema_version="1.0",
        generated_at=datetime.now(UTC),
        product=product,
        audience=audience,
        creative_brief=brief,
        claims_ledger=_claims(product),
        product_descriptions=_descriptions(product, brief),
        promotional_text=_promotion(product, brief),
        social_media=_social(product, brief, profile.name),
        visual_concepts=_visuals(product, brief),
        video_narration=_video(product, brief),
        compliance_warnings=[],
        consistency_warnings=[],
        quality_score=100,
    )
    return review_package(package)
