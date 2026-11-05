"""Provider interfaces for offline and future hosted generation."""

from abc import ABC, abstractmethod

from adforge.models import AdPackage, AudienceSelection, ProductInput


class LLMProvider(ABC):
    """Interface implemented by deterministic and hosted providers."""

    @abstractmethod
    def generate(self, product: ProductInput, audience: AudienceSelection) -> AdPackage:
        """Generate one validated package."""


class TemplateProvider(LLMProvider):
    """Offline deterministic provider used by default."""

    def generate(self, product: ProductInput, audience: AudienceSelection) -> AdPackage:
        """Generate a package from supplied facts without network access."""
        from .pipeline import generate_package

        return generate_package(product, audience)
