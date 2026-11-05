from adforge.config import Settings
from adforge.generation import TemplateProvider, provider_for
from adforge.models import AudienceSelection, ProductInput


def test_external_provider_is_opt_in() -> None:
    settings = Settings(llm_provider="openai", llm_api_key="not-used")
    assert isinstance(provider_for(settings), TemplateProvider)


def test_template_provider_remains_available_without_key() -> None:
    product = ProductInput(
        name="Lamp",
        category="lighting",
        key_features=["adjustable", "portable", "USB-C"],
        unique_selling_point="Focused light.",
        brand_name="Brand",
        brand_tone="trustworthy",
    )
    package = provider_for(Settings()).generate(
        product, AudienceSelection(preset="seniors")
    )
    assert package.product.name == "Lamp"
