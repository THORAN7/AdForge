"""FastAPI application entry point and stable health endpoint."""

from fastapi import FastAPI

from adforge import __version__
from adforge.config import get_settings
from adforge.models import GenerateRequest

settings = get_settings()
app = FastAPI(title=settings.app_name, version=__version__)


@app.get("/")
def root() -> dict[str, str]:
    """Provide a useful landing response for local development."""
    return {
        "service": settings.app_name,
        "version": __version__,
        "message": "AdForge API is running.",
        "health": "/api/health",
        "docs": "/docs",
    }


@app.get("/api/health")
def health() -> dict[str, str]:
    """Report service availability without exposing secrets or configuration."""
    return {"status": "ok", "service": settings.app_name, "version": __version__}


@app.post("/api/generate", status_code=501)
def generate(_: GenerateRequest) -> dict[str, str]:
    """Reserve the generation contract for the next implementation phase."""
    return {
        "error": "generation_not_implemented",
        "message": "Phase 3 adds generation.",
    }


def run() -> None:
    """Run the local development server."""
    import uvicorn

    uvicorn.run("adforge.api:app", host=settings.host, port=settings.port, reload=False)
