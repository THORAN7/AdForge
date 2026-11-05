"""Image-provider interface for future external image generation."""

from abc import ABC, abstractmethod


class ImageProvider(ABC):
    """Interface for providers that render visual concepts."""

    @abstractmethod
    def render(self, prompt: str, negative_prompt: str = "") -> bytes:
        """Return image bytes for a concept."""


class LocalImageProvider(ImageProvider):
    """Offline provider that returns no raster image and relies on SVG previews."""

    def render(self, prompt: str, negative_prompt: str = "") -> bytes:
        """Keep local mode deterministic and free of external image APIs."""
        return b""
