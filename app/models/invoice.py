from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Party(StrictModel):
    name: str | None = None
    address: str | None = None
    gstin: str | None = None
    state: str | None = None
    state_code: str | None = None


class InvoiceMetadata(StrictModel):
    number: str | None = None
    date: date | None = None
    document_type: Literal["tax_invoice", "credit_note", "debit_note", "unknown"] = "unknown"
    irn: str | None = None
    acknowledgement_number: str | None = None
    acknowledgement_date: date | None = None
    currency: str = "INR"


class InvoiceItem(StrictModel):
    description: str | None = None
    hsn_sac: str | None = None
    quantity: Decimal | None = None
    unit: str | None = None
    rate: Decimal | None = None
    taxable_value: Decimal | None = None
    discount: Decimal | None = None
    cgst_rate: Decimal | None = None
    cgst_amount: Decimal | None = None
    sgst_rate: Decimal | None = None
    sgst_amount: Decimal | None = None
    igst_rate: Decimal | None = None
    igst_amount: Decimal | None = None


class TaxSummary(StrictModel):
    taxable_value: Decimal | None = None
    cgst_rate: Decimal | None = None
    cgst_amount: Decimal | None = None
    sgst_rate: Decimal | None = None
    sgst_amount: Decimal | None = None
    igst_rate: Decimal | None = None
    igst_amount: Decimal | None = None
    total_tax: Decimal | None = None
    grand_total: Decimal | None = None
    amount_in_words: str | None = None
    tax_amount_in_words: str | None = None


class InvoiceExtraction(StrictModel):
    seller: Party = Field(default_factory=Party)
    buyer: Party = Field(default_factory=Party)
    invoice: InvoiceMetadata = Field(default_factory=InvoiceMetadata)
    items: list[InvoiceItem] = Field(default_factory=list)
    tax_summary: TaxSummary = Field(default_factory=TaxSummary)


class FieldConfidence(StrictModel):
    field: str
    level: Literal["high", "medium", "low", "unknown"]
    reason: str


class ValidationIssue(StrictModel):
    code: str
    severity: Literal["info", "warning", "error"]
    message: str
    field: str | None = None


class ValidationSummary(StrictModel):
    is_consistent: bool
    issues: list[ValidationIssue] = Field(default_factory=list)
    calculated_values: dict[str, str] = Field(default_factory=dict)


class ExtractionResponse(StrictModel):
    provider: str
    model: str
    extraction: InvoiceExtraction
    confidence: list[FieldConfidence]
    validation: ValidationSummary
    attempts: int
    latency_ms: int
    estimated_cost_usd: float | None = None
    notes: list[str] = Field(default_factory=list)
