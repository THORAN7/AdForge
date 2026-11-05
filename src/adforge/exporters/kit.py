"""ZIP campaign-kit export."""

from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile

from adforge.exporters.json_export import to_json
from adforge.exporters.markdown import to_markdown
from adforge.models import AdPackage


def to_zip(package: AdPackage) -> bytes:
    """Bundle canonical text, SSML, and local SVG previews."""
    output = BytesIO()
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        archive.writestr("package.json", to_json(package))
        archive.writestr("package.md", to_markdown(package))
        archive.writestr("video.ssml", package.video_narration.ssml)
        for index, svg in enumerate(package.visual_concepts.svg_previews, start=1):
            archive.writestr(f"visuals/preview-{index}.svg", svg)
    return output.getvalue()
