from io import BytesIO

import fitz
import pytesseract

from PIL import Image, ImageOps, ImageEnhance


def _preprocess_image(image: Image.Image) -> Image.Image:
    """Improve image quality before OCR"""

    image = ImageOps.grayscale(image)
    image = ImageOps.autocontrast(image)
    image = ImageEnhance.Contrast(image).enhance(0.5)

    return image


def extract_image_text(content: bytes) -> str:
    """Extract text from JPG/PNG images using Tesseract."""

    try:
        image = Image.open(BytesIO(content))
        image = _preprocess_image(image)

        return pytesseract.image_to_string(image, config="--psm 6").strip()

    except Exception as exc:
        raise ValueError(f"Image OCR failed: {exc}") from exc


def extract_pdf_using_ocr(content: bytes) -> str:
    """Render scannned PDF pages and extract text using OCR"""

    try:
        extracted_pages = []

        with fitz.open(stream=content, filetype="pdf") as document:
            for page_number, page in enumerate(document, start=1):
                pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)

                image = Image.open(BytesIO(pixmap.tobytes("png")))

                image = _preprocess_image(image)

                text = pytesseract.image_to_string(image, config="--psm 6").strip()

                if text:
                    extracted_pages.append(f"[Page {page_number}]\n{text}")

        return "\n\n".join(extracted_pages)

    except Exception as exc:
        raise ValueError(f"Scanned PDF OCR failed: ${exc}") from exc
