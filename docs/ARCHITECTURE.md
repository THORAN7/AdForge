# Architecture

AdForge uses a `src/` layout with FastAPI at the edge, typed Pydantic models at
the boundaries, a staged generation pipeline, automated checkers, and exporters
that consume one canonical `AdPackage`.

