from typing import List
try:
    from langchain_community.llms import Ollama
except ImportError:
    try:
        from langchain_ollama import ChatOllama as Ollama
    except ImportError:
        from langchain.llms import Ollama
try:
    from langchain_core.prompts import PromptTemplate
except ImportError:
    from langchain.prompts import PromptTemplate
from src.config import settings
from src.models import SourceChunk


class LLMService:
    def __init__(
        self,
        model_name: str = settings.llm_model_name,
        base_url: str = settings.llm_base_url,
        temperature: float = settings.llm_temperature,
        top_k: int = settings.llm_top_k,
        top_p: float = settings.llm_top_p,
    ) -> None:
        self.llm = Ollama(
            model=model_name,
            base_url=base_url,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
        )
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are a precise assistant that answers questions based exclusively on the provided context.

Context Information:
{context}

Question: {question}

Instructions:
- Answer using ONLY the information from the context above
- If the context does not contain sufficient information to answer, explicitly state that
- Cite the source(s) you used in your answer (e.g., Source 1, Source 2)
- Be factual, precise, and concise
- Do not make up information or use knowledge outside the provided context

Answer:""",
        )

    def generate_response(
        self, question: str, context_chunks: List[SourceChunk]
    ) -> str:
        if not context_chunks:
            return "No relevant context found in the knowledge base to answer this question."

        context_parts = []
        for i, chunk in enumerate(context_chunks, 1):
            context_parts.append(
                f"[Source {i} - Relevance Score: {chunk.score:.3f}]\n"
                f"Source: {chunk.source}\n"
                f"Content: {chunk.content}\n"
            )

        context = "\n---\n".join(context_parts)

        prompt = self.prompt_template.format(context=context, question=question)
        
        if hasattr(self.llm, 'invoke'):
            response = self.llm.invoke(prompt)
        else:
            response = self.llm(prompt)
        
        if isinstance(response, str):
            return response.strip()
        return str(response).strip()

