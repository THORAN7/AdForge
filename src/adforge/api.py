"""FastAPI application entry point and local web interface."""

from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from starlette.types import ASGIApp, Receive, Scope, Send

from adforge import __version__
from adforge.audiences import list_profiles
from adforge.config import Settings, get_settings
from adforge.exporters import to_docx, to_json, to_markdown, to_pdf, to_zip
from adforge.generation import provider_for
from adforge.models import AdPackage, AudienceProfile, GenerateRequest


class RequestSizeLimitMiddleware:
    """Reject requests larger than the configured limit before body parsing."""

    def __init__(self, app: ASGIApp, max_bytes: int) -> None:
        self.app = app
        self.max_bytes = max_bytes

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            content_length = next(
                (
                    value
                    for key, value in scope.get("headers", [])
                    if key.lower() == b"content-length"
                ),
                None,
            )
            if content_length is not None:
                try:
                    too_large = int(content_length) > self.max_bytes
                except ValueError:
                    too_large = True
                if too_large:
                    response = JSONResponse(
                        {
                            "error": "request_too_large",
                            "message": "Request exceeds the configured size limit.",
                            "details": {"max_bytes": self.max_bytes},
                        },
                        status_code=413,
                    )
                    await response(scope, receive, send)
                    return
        await self.app(scope, receive, send)


def _error(
    error: str, message: str, details: object = None, status_code: int = 500
) -> JSONResponse:
    return JSONResponse(
        {"error": error, "message": message, "details": details},
        status_code=status_code,
    )


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build an application instance with explicitly supplied test settings."""
    runtime_settings = settings or get_settings()
    static_dir = Path(__file__).parent / "static"

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        yield

    application = FastAPI(
        title=runtime_settings.app_name,
        version=__version__,
        lifespan=lifespan,
    )
    application.add_middleware(
        RequestSizeLimitMiddleware, max_bytes=runtime_settings.max_upload_bytes
    )

    @application.middleware("http")
    async def security_headers(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; style-src 'self' 'unsafe-inline'; "
            "script-src 'self' 'unsafe-inline'; img-src 'self' data:"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        return response

    @application.exception_handler(RequestValidationError)
    async def validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
        fields = "; ".join(
            f"{'.'.join(str(part) for part in error['loc'])}: {error['msg']}"
            for error in exc.errors()
        )
        return _error(
            "validation_error",
            f"Request validation failed. {fields}",
            {"errors": exc.errors()},
            422,
        )

    @application.exception_handler(HTTPException)
    async def http_error(_: Request, exc: HTTPException) -> JSONResponse:
        return _error("http_error", str(exc.detail), None, exc.status_code)

    @application.exception_handler(Exception)
    async def unhandled_error(_: Request, __: Exception) -> JSONResponse:
        return _error("internal_error", "An unexpected error occurred.", None, 500)

    @application.get("/")
    def root() -> FileResponse:
        """Serve the local browser landing page."""
        return FileResponse(
            static_dir / "index.html",
            media_type="text/html",
            headers={"Cache-Control": "no-store, max-age=0"},
        )

    @application.get("/api/health")
    def health() -> dict[str, str]:
        """Report service availability without exposing secrets or configuration."""
        return {
            "status": "ok",
            "service": runtime_settings.app_name,
            "version": __version__,
        }

    @application.get("/api/audiences", response_model=list[AudienceProfile])
    def audiences() -> list[AudienceProfile]:
        """List the documented audience presets."""
        return list_profiles()

    @application.post("/api/generate", response_model=list[AdPackage])
    def generate(request: GenerateRequest) -> list[AdPackage]:
        """Generate one deterministic package per selected audience."""
        provider = provider_for(runtime_settings)
        return [
            provider.generate(request.product, audience)
            for audience in request.audiences
        ]

    @application.post("/api/generate/compare", response_model=list[AdPackage])
    def compare(request: GenerateRequest) -> list[AdPackage]:
        """Generate packages for side-by-side audience comparison."""
        provider = provider_for(runtime_settings)
        return [
            provider.generate(request.product, audience)
            for audience in request.audiences
        ]

    @application.post("/api/regenerate/{section}", response_model=list[AdPackage])
    def regenerate(section: str, request: GenerateRequest) -> list[AdPackage]:
        """Regenerate a supported section while preserving the package contract."""
        valid_sections = {
            "product_descriptions",
            "promotional_text",
            "social_media",
            "visual_concepts",
            "video_narration",
        }
        if section not in valid_sections:
            raise HTTPException(
                status_code=422,
                detail=f"unsupported section: {section}",
            )
        provider = provider_for(runtime_settings)
        return [
            provider.generate(request.product, audience)
            for audience in request.audiences
        ]

    @application.post("/api/export/{format_name}")
    def export_package(format_name: str, request: GenerateRequest) -> Response:
        """Generate one package and export it in the requested format."""
        package = provider_for(runtime_settings).generate(
            request.product, request.audiences[0]
        )
        exporters = {
            "json": (to_json, "application/json", "package.json"),
            "markdown": (to_markdown, "text/markdown", "package.md"),
            "docx": (
                to_docx,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "package.docx",
            ),
            "pdf": (to_pdf, "application/pdf", "package.pdf"),
            "zip": (to_zip, "application/zip", "campaign-kit.zip"),
        }
        if format_name not in exporters:
            raise HTTPException(status_code=422, detail="unsupported export format")
        exporter, media_type, filename = exporters[format_name]
        return Response(
            content=exporter(package),
            media_type=media_type,
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

    application.mount("/static", StaticFiles(directory=static_dir), name="static")
    return application


app = create_app()


def run() -> None:
    """Run the local development server."""
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "adforge.api:app",
        host=settings.host,
        port=settings.port,
        reload=False,
    )
