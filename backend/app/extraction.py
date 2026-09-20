"""Extraction de texte brut à partir des fichiers PDF/DOCX stockés."""

from pathlib import Path

import pdfplumber
from docx import Document


def extract_text(path: Path) -> str:
    """Extrait le texte brut d'un fichier PDF ou DOCX."""
    extension = path.suffix.lower()
    if extension == ".pdf":
        return _extract_from_pdf(path)
    if extension == ".docx":
        return _extract_from_docx(path)
    raise ValueError(f"Extraction non supportée pour l'extension '{extension}'.")


def _extract_from_pdf(path: Path) -> str:
    pages_text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            pages_text.append(page.extract_text() or "")
    return "\n\n".join(pages_text).strip()


def _extract_from_docx(path: Path) -> str:
    document = Document(path)
    return "\n".join(paragraph.text for paragraph in document.paragraphs).strip()
