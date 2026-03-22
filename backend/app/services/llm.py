from openai import OpenAI
from app.core.config import settings
from typing import List, Dict, Any

class LLMService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = OpenAI(api_key=self.api_key)
        return self._client

    def generate_answer(self, query: str, context_chunks: List[Dict[str, Any]]) -> str:
        if not context_chunks:
            return "I'm sorry, I couldn't find any relevant information to answer your question."

        # Combine chunks into a single context string
        context_text = "\n\n".join([f"Source {i+1}:\n{chunk['content']}" for i, chunk in enumerate(context_chunks)])

        prompt = f"""
        You are a helpful assistant. Answer the user's question using ONLY the provided context.
        If the answer is not in the context, say that you don't know based on the provided documents.

        CONTEXT:
        {context_text}

        USER QUESTION:
        {query}

        ANSWER:
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini", # Good production baseline for speed/cost
                messages=[
                    {"role": "system", "content": "You are a professional research assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1 # Low temperature for factual RAG responses
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating answer: {str(e)}"

llm_service = LLMService()
