"""Dependency-free SVG preview cards."""

from html import escape


def _card(title: str, subtitle: str, accent: str) -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="360" '
        'viewBox="0 0 640 360" role="img">'
        f'<rect width="640" height="360" fill="{accent}"/>'
        '<rect x="28" y="28" width="584" height="304" rx="18" '
        'fill="#0b1020" opacity=".82"/>'
        f'<text x="56" y="110" fill="#ffffff" font-size="30" '
        f'font-family="Arial,sans-serif">{escape(title)}</text>'
        f'<text x="56" y="160" fill="#cbd5e1" font-size="18" '
        f'font-family="Arial,sans-serif">{escape(subtitle)}</text>'
        '<text x="56" y="292" fill="#7dd3fc" font-size="14" '
        'font-family="Arial,sans-serif">AdForge local preview</text></svg>'
    )


def render_preview_cards(
    product_name: str, storyboard: list[str], palette: list[str]
) -> list[str]:
    """Render one poster card and up to eight storyboard cards."""
    accent = palette[0] if palette else "#1e3a8a"
    cards = [_card(product_name, "Poster layout preview", accent)]
    cards.extend(
        _card(
            f"Storyboard {index}",
            frame,
            palette[index % len(palette)] if palette else accent,
        )
        for index, frame in enumerate(storyboard, start=1)
    )
    return cards[:9]
