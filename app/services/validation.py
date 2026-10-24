from decimal import Decimal, ROUND_HALF_UP

from app.models.invoice import InvoiceExtraction, ValidationIssue, ValidationSummary


CENT = Decimal("0.01")


def money(value: Decimal) -> Decimal:
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def _add_issue(issues, code, severity, message, field=None):
    issues.append(ValidationIssue(code=code, severity=severity, message=message, field=field))


def validate_invoice(invoice: InvoiceExtraction) -> ValidationSummary:
    """Run deterministic arithmetic and basic format checks; not a GST compliance opinion."""
    issues: list[ValidationIssue] = []
    calculated: dict[str, str] = {}

    if not invoice.items:
        _add_issue(issues, "NO_LINE_ITEMS", "warning", "No line items were extracted.", "items")

    item_taxable_values = [
        item.taxable_value for item in invoice.items if item.taxable_value is not None
    ]
    if item_taxable_values and len(item_taxable_values) == len(invoice.items):
        line_total = money(sum(item_taxable_values, Decimal("0")))
        calculated["line_items_taxable_total"] = str(line_total)
        if invoice.tax_summary.taxable_value is not None:
            declared = money(invoice.tax_summary.taxable_value)
            if line_total != declared:
                _add_issue(
                    issues,
                    "TAXABLE_TOTAL_MISMATCH",
                    "error",
                    f"Line-item taxable total ({line_total}) differs from declared taxable value ({declared}).",
                    "tax_summary.taxable_value",
                )

    summary = invoice.tax_summary
    tax_parts = [summary.cgst_amount, summary.sgst_amount, summary.igst_amount]
    present_tax_parts = [value for value in tax_parts if value is not None]
    if present_tax_parts:
        calculated_tax = money(sum(present_tax_parts, Decimal("0")))
    calculated["calculated_total_tax"] = str(calculated_tax)
    if summary.total_tax is not None and calculated_tax != money(summary.total_tax):
        _add_issue(
            issues,
            "TAX_TOTAL_MISMATCH",
            "error",
            f"Component taxes total {calculated_tax}, but declared total tax is {money(summary.total_tax)}.",
            "tax_summary.total_tax",
        )

    if summary.taxable_value is not None and summary.total_tax is not None:
        calculated_grand = money(summary.taxable_value + summary.total_tax)
        calculated["calculated_grand_total"] = str(calculated_grand)
        if summary.grand_total is not None and calculated_grand != money(summary.grand_total):
            _add_issue(
                issues,
                "GRAND_TOTAL_MISMATCH",
                "error",
                f"Taxable value plus tax is {calculated_grand}, but declared grand total is {money(summary.grand_total)}.",
                "tax_summary.grand_total",
            )

        # GSTIN shape check only. This does not establish that a GSTIN is registered or valid.
    for party_name, party in (("seller", invoice.seller), ("buyer", invoice.buyer)):
        gstin = party.gstin
        if gstin:
            normalized = gstin.strip().upper()
            if len(normalized) != 15:
                _add_issue(
                    issues,
                    "GSTIN_LENGTH",
                    "warning",
                    f"{party_name.title()} GSTIN has {len(normalized)} characters; expected 15.",
                    f"{party_name}.gstin",
                )
            elif not normalized[:2].isdigit():
                _add_issue(
                    issues,
                    "GSTIN_STATE_PREFIX",
                    "warning",
                    f"{party_name.title()} GSTIN does not start with a two-digit state code.",
                    f"{party_name}.gstin",
                )

    is_consistent = not any(issue.severity == "error" for issue in issues)
    return ValidationSummary(
        is_consistent=is_consistent,
        issues=issues,
        calculated_values=calculated,
    )
