from decimal import Decimal

import pytest
from pydantic import ValidationError

from adforge.models import AudienceSelection, GenerateRequest, ProductInput


def test_generate_request_accepts_three_to_eight_features() -> None:
    product = ProductInput(
        name="Focus Lamp",
        category="desk lighting",
        key_features=["adjustable", "portable", "USB-C"],
        unique_selling_point="Focused light for flexible workspaces.",
        brand_name="Northstar",
        brand_tone="trustworthy",
    )
    request = GenerateRequest(
        product=product,
        audiences=[AudienceSelection(preset="gen_z_students")],
    )
    assert request.product.name == "Focus Lamp"


def product_data(**overrides: object) -> dict[str, object]:
    data: dict[str, object] = {
        "name": "Focus Lamp",
        "category": "desk lighting",
        "key_features": ["adjustable", "portable", "USB-C"],
        "unique_selling_point": "Focused light for flexible workspaces.",
        "brand_name": "Northstar",
        "brand_tone": "trustworthy",
    }
    data.update(overrides)
    return data


@pytest.mark.parametrize(
    "audience",
    [
        {},
        {
            "preset": "gen_z_students",
            "custom": {"age_range": "18-24", "interests": ["study"]},
        },
        {"preset": "unknown"},
    ],
)
def test_audience_selection_rejects_invalid_sources(
    audience: dict[str, object],
) -> None:
    with pytest.raises(ValidationError):
        AudienceSelection.model_validate(audience)


@pytest.mark.parametrize(
    "features",
    [
        ["one", "two"],
        ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"],
    ],
)
def test_product_rejects_feature_count_outside_range(features: list[str]) -> None:
    with pytest.raises(ValidationError):
        ProductInput.model_validate(product_data(key_features=features))


def test_product_rejects_bad_hex_color() -> None:
    with pytest.raises(ValidationError):
        ProductInput.model_validate(product_data(brand_colors=["blue"]))


def test_product_rejects_oversized_string() -> None:
    with pytest.raises(ValidationError):
        ProductInput.model_validate(product_data(name="x" * 121))


def test_product_parses_structured_offer() -> None:
    product = ProductInput.model_validate(product_data(price_offer="$19.99, 20% off"))
    assert product.offer is not None
    assert product.offer.amount == Decimal("19.99")
    assert product.offer.currency == "USD"
    assert product.offer.discount_percent == 20


def test_product_rejects_invalid_language() -> None:
    with pytest.raises(ValidationError):
        ProductInput.model_validate(
            product_data(language="English language with spaces")
        )
