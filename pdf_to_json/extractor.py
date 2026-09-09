"""PDF extraction logic kept separate from the command-line interface."""

from pathlib import Path
from typing import Any

from pypdf import PdfReader


def _metadata(reader: PdfReader) -> dict[str, Any]:
    metadata = reader.metadata or {}
    return {
        str(key).lstrip("/"): value
        for key, value in metadata.items()
        if value is not None
    }


def _form_fields(reader: PdfReader) -> dict[str, Any]:
    fields = reader.get_fields() or {}
    return {
        name: field.get("/V")
        for name, field in fields.items()
        if field.get("/V") is not None
    }


def extract_pdf(path: str | Path) -> dict[str, Any]:
    """Extract metadata, form fields and page text from *path*."""
    pdf_path = Path(path)
    reader = PdfReader(str(pdf_path))

    pages = [
        {"number": page_number, "text": page.extract_text() or ""}
        for page_number, page in enumerate(reader.pages, start=1)
    ]

    return {
        "file": pdf_path.name,
        "pages_count": len(pages),
        "metadata": _metadata(reader),
        "form_fields": _form_fields(reader),
        "pages": pages,
    }