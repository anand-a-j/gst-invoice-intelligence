from app.services.documents.image_ocr import (
    extract_image_text,
    extract_pdf_using_ocr,
)
from app.services.documents.pdf_extractor import extract_pdf_text


def extract_text_from_pdf(content: bytes) -> tuple[str, str]:
    """
    Extract PDF text.

    Returns:
        tupl[str, str]: Extracted text and extration method
    """

    text = extract_pdf_text(content=content)

    if text.strip():
        return text, "pdf_text"

    text = extract_pdf_using_ocr(content=content)

    if not text.strip():
        raise ValueError(
            "No readable text found in PDF"
        )

    return text, "pdf_ocr"


def extract_text_from_image(content: bytes) -> tuple[str, str]:
    """
    Extract text from an image.

    Returns:
        tuple[str, str]: Extracted text and extraction method.
    """

    text = extract_image_text(content=content)

    if not text.strip():
        raise ValueError(
            "No readable text found in image"
        )

    return text, "image_ocr"