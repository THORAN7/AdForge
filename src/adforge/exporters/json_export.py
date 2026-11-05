"""JSON export."""

import json

from adforge.models import AdPackage


def to_json(package: AdPackage) -> bytes:
    """Serialize the canonical package without recomputing any content."""
    return json.dumps(
        package.model_dump(mode="json"), indent=2, ensure_ascii=False
    ).encode("utf-8")
