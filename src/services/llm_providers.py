from abc import ABC, abstractmethod
from typing import List
from src.models import SourceChunk


class BaseLLMProvider(ABC):
    @abstractmethod
    def generate_response(self, question: str, context_chunks: List[SourceChunk]) -> str:
        pass

    def _build_context(self, context_chunks: List[SourceChunk]) -> str:
        if not context_chunks:
            return ""

        context_parts = []
        for i, chunk in enumerate(context_chunks, 1):
            context_parts.append(
                f"[Source {i} - Score: {chunk.score:.3f}]\n"
                f"Source: {chunk.source}\n"
                f"Content: {chunk.content}\n"
            )
        return "\n---\n".join(context_parts)


class OllamaProvider(BaseLLMProvider):
    def __init__(self, model_name: str, base_url: str, temperature: float = 0.0):
        try:
            from langchain_community.llms import Ollama
        except ImportError:
            from langchain_ollama import ChatOllama as Ollama

        self.llm = Ollama(
            model=model_name,
            base_url=base_url,
            temperature=temperature,
        )

    def generate_response(self, question: str, context_chunks: List[SourceChunk]) -> str:
        if not context_chunks:
            return "No relevant context found in the knowledge base."

        context = self._build_context(context_chunks)
        prompt = f"""Answer based exclusively on the context below.

Context:
{context}

Question: {question}

Answer:"""

        response = self.llm.invoke(prompt) if hasattr(self.llm, 'invoke') else self.llm(prompt)
        return str(response).strip()


class OpenAIProvider(BaseLLMProvider):
    def __init__(self, model_name: str = "gpt-4o-mini", api_key: str = None, temperature: float = 0.0):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)
        self.model = model_name
        self.temperature = temperature

    def generate_response(self, question: str, context_chunks: List[SourceChunk]) -> str:
        if not context_chunks:
            return "No relevant context found in the knowledge base."

        context = self._build_context(context_chunks)

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based exclusively on the provided context. Cite sources in your answer."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
            ]
        )
        return response.choices[0].message.content.strip()


class AnthropicProvider(BaseLLMProvider):
    def __init__(self, model_name: str = "claude-3-5-sonnet-20241022", api_key: str = None, temperature: float = 0.0):
        from anthropic import Anthropic
        self.client = Anthropic(api_key=api_key)
        self.model = model_name
        self.temperature = temperature

    def generate_response(self, question: str, context_chunks: List[SourceChunk]) -> str:
        if not context_chunks:
            return "No relevant context found in the knowledge base."

        context = self._build_context(context_chunks)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            temperature=self.temperature,
            messages=[
                {"role": "user", "content": f"Answer based exclusively on this context. Cite sources.\n\nContext:\n{context}\n\nQuestion: {question}"}
            ]
        )
        return response.content[0].text.strip()


def get_llm_provider(provider_type: str, **kwargs) -> BaseLLMProvider:
    providers = {
        'ollama': OllamaProvider,
        'openai': OpenAIProvider,
        'anthropic': AnthropicProvider,
    }

    provider_class = providers.get(provider_type.lower())
    if not provider_class:
        raise ValueError(f"Unknown provider: {provider_type}. Supported: {list(providers.keys())}")

    return provider_class(**kwargs)
