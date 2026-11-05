"""Platform and narration boundary checks."""

from adforge.models import AdPackage


def check_platforms(package: AdPackage) -> list[str]:
    """Validate limits not fully expressible in Pydantic field bounds."""
    warnings: list[str] = []
    social = package.social_media
    if len(social.instagram.hashtags) > 30:
        warnings.append("Instagram hashtag limit exceeded")
    if len(social.x.post) > 280:
        warnings.append("X post limit exceeded")
    ads = package.promotional_text.google_ads
    if any(len(headline) > 30 for headline in ads.headlines):
        warnings.append("Google Ads headline limit exceeded")
    if any(len(description) > 90 for description in ads.descriptions):
        warnings.append("Google Ads description limit exceeded")
    return warnings
