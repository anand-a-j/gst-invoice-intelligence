from app.core.config import Settings
from app.providers.base import InvoiceLLMProvider
from app.providers.openai_provider import OpenAIInvoiceProvider


def create_provider(settings: Settings) -> InvoiceLLMProvider:
    if settings.llm_provider == "openai":
        if not settings.openai_api_key.get_secret_value():
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
        return OpenAIInvoiceProvider(settings)

    raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")
