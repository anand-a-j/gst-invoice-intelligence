from openai import AsyncOpenAI

from app.core.config import Settings
from app.models.invoice import InvoiceExtraction
from app.providers.base import ProviderResult
from app.providers.prompts import SYSTEM_PROMPT, build_user_prompt


class OpenAIInvoiceProvider:
    name = "openai"

    def __init__(self, settings: Settings):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.temperature = settings.llm_temperature

    async def extract(self, invoice_text: str, correction_feedback: str = "") -> ProviderResult:
        response = await self.client.responses.parse(
            model=self.model,
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(invoice_text, correction_feedback)},
            ],
            text_format=InvoiceExtraction,
            temperature=self.temperature,
        )
        parsed = response.output_parsed
        if parsed is None:
            raise ValueError("OpenAI returned no parsed structured output.")

        usage = getattr(response, "usage", None)
        return ProviderResult(
            extration=parsed,
            model=self.model,
            input_tokens=getattr(usage, "input_tokens", None) if usage else None,
            output_tokens=getattr(usage, "output_tokens", None) if usage else None,
        )
