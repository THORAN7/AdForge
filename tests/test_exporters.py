from io import BytesIO
from zipfile import ZipFile

from adforge.exporters import to_docx, to_json, to_markdown, to_pdf, to_zip
from adforge.generation import TemplateProvider
from adforge.models import AudienceSelection, ProductInput


def package():
    product = ProductInput(
        name="Desk Lamp",
        category="lighting",
        key_features=["adjustable", "portable", "USB-C"],
        price_offer="$19.99",
        unique_selling_point="Focused light.",
        brand_name="BrightCo",
        brand_tone="trustworthy",
    )
    return TemplateProvider().generate(
        product, AudienceSelection(preset="young_professionals")
    )


def test_text_and_document_exports_preserve_key_facts() -> None:
    item = package()
    assert b"Desk Lamp" in to_json(item)
    assert b"Desk Lamp" in to_markdown(item)
    with ZipFile(BytesIO(to_docx(item))) as document:
        assert b"Desk Lamp" in document.read("word/document.xml")
    assert to_pdf(item).startswith(b"%PDF")


def test_zip_contains_canonical_assets() -> None:
    item = package()
    with ZipFile(BytesIO(to_zip(item))) as archive:
        names = archive.namelist()
        assert "package.json" in names
        assert "package.md" in names
        assert "video.ssml" in names
        assert any(name.endswith(".svg") for name in names)
