from dataclasses import dataclass
from typing import Protocol

from app.models.invoice import InvoiceExtraction


@dataclass
class ProviderResult:
    extration: InvoiceExtraction
    model: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    estimated_cost_usd: float | None = None


class InvoiceLLMProvider(Protocol):
    name: str
    model: str

    async def extract(self, invoice_text: str, correction_feedback: str = "") -> ProviderResult:
        """Extract invoice fields into the shared Pydantic schema.""" 