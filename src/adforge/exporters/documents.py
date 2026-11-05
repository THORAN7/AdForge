"""Optional DOCX and PDF exports."""

from io import BytesIO

from adforge.models import AdPackage

from .markdown import to_markdown


def to_docx(package: AdPackage) -> bytes:
    """Create a DOCX document from the canonical package."""
    try:
        from docx import Document
    except ImportError as exc:
        raise RuntimeError("Install the documents extra to export DOCX.") from exc
    document = Document()
    document.add_heading(package.product.name, 0)
    for line in to_markdown(package).decode("utf-8").splitlines():
        if line.startswith("# "):
            continue
        if line.startswith("## "):
            document.add_heading(line[3:], level=1)
        elif line.startswith("### "):
            document.add_heading(line[4:], level=2)
        elif line.startswith("- "):
            document.add_paragraph(line[2:], style="List Bullet")
        elif line.strip():
            document.add_paragraph(line.replace("**", ""))
    output = BytesIO()
    document.save(output)
    return output.getvalue()


def to_pdf(package: AdPackage) -> bytes:
    """Create a simple PDF document from the canonical package."""
    try:
        from reportlab.lib.pagesizes import letter  # type: ignore[import-untyped]
        from reportlab.pdfgen.canvas import Canvas  # type: ignore[import-untyped]
    except ImportError as exc:
        raise RuntimeError("Install the documents extra to export PDF.") from exc
    output = BytesIO()
    canvas = Canvas(output, pagesize=letter)
    _, height = letter
    y = height - 48
    canvas.setFont("Helvetica-Bold", 16)
    canvas.drawString(48, y, package.product.name)
    canvas.setFont("Helvetica", 9)
    for line in to_markdown(package).decode("utf-8").splitlines():
        if line.startswith("# "):
            continue
        if y < 48:
            canvas.showPage()
            y = height - 48
        canvas.drawString(48, y, line.replace("**", "")[:110])
        y -= 13
    canvas.save()
    return output.getvalue()
