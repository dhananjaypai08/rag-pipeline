from typing import List
from src.config import settings
from src.models import SourceChunk
from src.services.llm_providers import get_llm_provider


class LLMService:
    def __init__(self):
        provider_type = settings.llm_provider.lower()

        if provider_type == 'ollama':
            self.provider = get_llm_provider(
                'ollama',
                model_name=settings.llm_model_name,
                base_url=settings.llm_base_url,
                temperature=settings.llm_temperature,
            )
        elif provider_type == 'openai':
            self.provider = get_llm_provider(
                'openai',
                model_name=settings.llm_model_name,
                api_key=settings.openai_api_key,
                temperature=settings.llm_temperature,
            )
        elif provider_type == 'anthropic':
            self.provider = get_llm_provider(
                'anthropic',
                model_name=settings.llm_model_name,
                api_key=settings.anthropic_api_key,
                temperature=settings.llm_temperature,
            )
        else:
            raise ValueError(f"Unknown LLM provider: {provider_type}")

    def generate_response(self, question: str, context_chunks: List[SourceChunk]) -> str:
        return self.provider.generate_response(question, context_chunks)
