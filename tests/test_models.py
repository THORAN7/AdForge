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

