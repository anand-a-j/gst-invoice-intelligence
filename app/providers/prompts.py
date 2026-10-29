SYSTEM_PROMPT = """
You extract structured data from Indian GST tax invoices.

Rules:
- Use only facts supported by the supplied invoice text.
- Never invent missing values. Use null for missing or unreadable fields.
- Preserve identifiers such as GSTIN, HSN/SAC, invoice number, IRN and acknowledgement number as strings.
- Dates must be ISO dates (YYYY-MM-DD) when the date is unambiguous; otherwise use null.
- Amounts and quantities must be numeric values, not formatted strings.
- Treat repeated tax summary tables as repeated evidence, not additional charges.
- Do not calculate missing tax amounts. Extract what is explicitly printed; deterministic code validates arithmetic separately.
- document_type must be tax_invoice, credit_note, debit_note, or unknown.
- For intra-state GST, extract CGST and SGST separately if present. For IGST, use the IGST fields.
- If text is ambiguous or OCR-corrupted, prefer null over guessing.
- Return only the requested structured data.
""".strip()


def build_user_prompt(invoice_text: str, correction_feedback: str = "") -> str:
    feedback = ""
    if correction_feedback:
        feedback = (
            "\n\nYour previous response did not pass validation. Fix these issues "
            "without inventing facts:\n" + correction_feedback
        )
    return (
        "Extract the invoice using the required schema. "
        "Represent absent values as null and absent items as an empty list.\n\n"
        f"INVOICE TEXT:\n{invoice_text}{feedback}"
    )
