
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    base_url="https://router.huggingface.co/novita/v3/openai",
    api_key=os.environ["HF_TOKEN"],
)




class RAGPipeline:
    def __init__(self, vector_store, top_k: int = 5):
        self.vector_store = vector_store
        self.top_k = top_k

    def run(self, query: str):
        try:
            relevant_chunks = self.vector_store.search(query, top_k=self.top_k)
            if not relevant_chunks:
                return {"answer": "No relevant context found.", "citations": []}
            context_texts = tuple(chunk["text"] for chunk in relevant_chunks)
            answer = generate_with_hf_llm(query, context_texts)
            citations = [
                {
                    "text": chunk["text"],
                    "source": chunk["source"],
                    "location": chunk.get("location", chunk.get("chunk_id", ""))
                }
                for chunk in relevant_chunks[:3]
            ]
            return {"answer": answer, "citations": citations}
        except Exception as e:
            return {"answer": f"Unexpected error: {str(e)}", "citations": []}



def generate_with_hf_llm(query: str, contexts: list[str]) -> str:
    try:
        prompt = (
            "You are an  expert assistant. Read the provided context and answer the question in your own words. use extracted texts from PDFs and Documents. Starts with yes or no if the question is a yes or no question.\n\n"
        )
        for i, ctx in enumerate(contexts[:2]):
            prompt += f"Context {i+1}: {ctx.strip()}\n"
        prompt += f"\nQuestion: {query.strip()}\nAnswer:"
        try:
            completion = client.chat.completions.create(
                model="baidu/ernie-4.5-21B-a3b",
                messages=[{"role": "user", "content": prompt}],
                timeout=20
            )
        except TypeError:
            completion = client.chat.completions.create(
                model="baidu/ernie-4.5-21B-a3b",
                messages=[{"role": "user", "content": prompt}]
            )
        llm_answer = completion.choices[0].message.content.strip()
        return llm_answer
    except Exception as e:
        return f"[LLM generation error: {str(e)}]"