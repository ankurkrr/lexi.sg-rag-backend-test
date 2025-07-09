from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from vector_store import PDFVectorStore
from rag_pipeline import RAGPipeline

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

# Initialize FAISS vector store for PDFs
doc_vector_store = PDFVectorStore(r"your pdf location",)

# Initialize RAG pipeline
rag_pipeline = RAGPipeline(doc_vector_store)

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    result = rag_pipeline.run(request.query)
    if not result["answer"]:
        raise HTTPException(status_code=404, detail="No relevant legal text found.")
    return result
