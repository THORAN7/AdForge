# Architecture

AdForge uses a `src/` layout with FastAPI at the edge, typed Pydantic models at
the boundaries, a staged generation pipeline, automated checkers, and exporters
that consume one canonical `AdPackage`.

Visuals are rendered locally as SVG preview cards by default. `ImageProvider` is
an interface boundary for an optional real image generator without making the
offline path depend on an external API.
