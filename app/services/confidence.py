from app.models.invoice import FieldConfidence, InvoiceExtraction


def assess_confidence(invoice: InvoiceExtraction, source_text: str) -> list[FieldConfidence]:
    """
    This function checks how reliable your GST invoice extraction is.

    It loops through key fields like seller name, GSTIN, invoice date, and total amount.

    Heuristic evidence indicator, not a calibrated probability.
    A field is high only when populated and its normalized value is visibly present in source text.
    """
    source = " ".join(source_text.lower()).split()
    fields: list[tuple[str, object]] = [
        ("seller.name", invoice.seller.name),
        ("seller.gstin", invoice.seller.gstin),
        ("buyer.name", invoice.buyer.name),
        ("buyer.gstin", invoice.buyer.gstin),
        ("invoice.number", invoice.invoice.number),
        ("invoice.date", invoice.invoice.date),
        ("tax_summary.taxable_value", invoice.tax_summary.taxable_value),
        ("tax_summary.total_tax", invoice.tax_summary.total_tax),
        ("tax_summary.grand_total", invoice.tax_summary.grand_total),
    ]
    results: list[FieldConfidence] = []

    for field, value in fields:
        if value is None or str(value).strip() == "":
            results.append(
                FieldConfidence(field=field, level="unknown", reason="Field was not extracted.")
            )
            continue

        normalized = " ".join(str(value).lower().split())
        compact_source = source.replace(" ", "")
        compact_value = normalized.replace(" ", "")
        if normalized in source or compact_value in compact_source:
            results.append(
                FieldConfidence(
                    field=field,
                    level="high",
                    reason="Extracted value appears in the supplied source text; this is not proof of correctness.",
                )
            )
        else:
            results.append(
                FieldConfidence(
                    field=field,
                    level="low",
                    reason="Extracted value was not found verbatim in the supplied text; review it.",
                )
            )

    return results
