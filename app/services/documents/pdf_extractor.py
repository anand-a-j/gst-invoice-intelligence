import fitz


def extract_pdf_text(content: bytes) -> str:
    """Extract embedded text from a digital PDF"""

    try:
        with fitz.open(stream=content, filetype="pdf") as document:
            pages = []

            for page_number, page in enumerate(document, start=1):
                text = page.get_text("text").strip()

                if text:
                    pages.append(f"[Page {page_number}]\n{text}")

            return "\n\n".join(pages)

    except Exception as exc:
        raise ValueError(f"Failed to read PDF: {exc}") from exc
