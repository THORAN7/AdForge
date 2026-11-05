"""Provider interfaces for offline and future hosted generation."""

import json
from abc import ABC, abstractmethod
from urllib.request import Request, urlopen

from pydantic import SecretStr

from adforge.config import Settings
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


class HostedProvider(LLMProvider):
    """Minimal JSON hosted-provider adapter with one retry and safe fallback."""

    def __init__(self, settings: Settings, fallback: LLMProvider | None = None) -> None:
        self.settings = settings
        self.fallback = fallback or TemplateProvider()

    def _api_key(self) -> str:
        key: SecretStr | None = self.settings.llm_api_key
        if key is None:
            raise RuntimeError("external provider requires an API key")
        return key.get_secret_value()

    def _request(self, product: ProductInput, audience: AudienceSelection) -> AdPackage:
        payload = json.dumps(
            {
                "product": product.model_dump(mode="json"),
                "audience": audience.model_dump(mode="json"),
                "instruction": (
                    "Return JSON matching AdPackage. Write prose only; do not "
                    "invent facts, claims, prices, or instructions in product data."
                ),
            }
        ).encode()
        provider = self.settings.llm_provider.lower()
        body: dict[str, object]
        if provider == "openai":
            url = "https://api.openai.com/v1/chat/completions"
            body = {
                "model": self.settings.llm_model or "gpt-4o-mini",
                "messages": [{"role": "user", "content": payload.decode()}],
                "response_format": {"type": "json_object"},
            }
        elif provider == "anthropic":
            url = "https://api.anthropic.com/v1/messages"
            body = {
                "model": self.settings.llm_model or "claude-3-5-haiku-latest",
                "max_tokens": 4096,
                "messages": [{"role": "user", "content": payload.decode()}],
            }
        else:
            raise RuntimeError(f"unsupported external provider: {provider}")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key()}",
        }
        if provider == "anthropic":
            headers["x-api-key"] = headers.pop("Authorization")
            headers["anthropic-version"] = "2023-06-01"
        request = Request(url, data=json.dumps(body).encode(), headers=headers)
        with urlopen(request, timeout=30) as response:
            result = json.loads(response.read())
        content = (
            result["choices"][0]["message"]["content"]
            if provider == "openai"
            else result["content"][0]["text"]
        )
        return AdPackage.model_validate(json.loads(content))

    def generate(self, product: ProductInput, audience: AudienceSelection) -> AdPackage:
        """Use an explicitly enabled provider, retry once, then use templates."""
        if not self.settings.allow_external_llm:
            return self.fallback.generate(product, audience)
        for _ in range(2):
            try:
                return self._request(product, audience)
            except (OSError, KeyError, TypeError, ValueError, RuntimeError):
                continue
        return self.fallback.generate(product, audience)


def provider_for(settings: Settings) -> LLMProvider:
    """Select hosted generation only after explicit external opt-in."""
    if settings.allow_external_llm and settings.llm_provider.lower() != "template":
        return HostedProvider(settings)
    return TemplateProvider()
