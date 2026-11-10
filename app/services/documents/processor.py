from app.services.documents.text_extractor import (
    extract_text_from_image,
    extract_text_from_pdf,
)

SUPPORTED_CONTENT_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
}


def process_document(
    content: bytes,
    content_type: str,
) -> tuple[str, str]:
    """
    Process an uploaded invoice document.

    Returns:
        tuple[str, str]: Extracted text and extraction method.
    """


    if not content:
        raise ValueError("Uploaded document is empty")

    if content_type not in SUPPORTED_CONTENT_TYPES:
        raise ValueError(
            "Unsupported file type. Upload PDF, JPG or PNG."
        )

    if content_type == "application/pdf":
        return extract_text_from_pdf(content=content)

    return extract_text_from_image(content=content)