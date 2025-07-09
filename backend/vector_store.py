import os
import faiss
import numpy as np
from PyPDF2 import PdfReader
from docx import Document
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
import pickle
from concurrent.futures import ThreadPoolExecutor, as_completed



class PDFVectorStore:
    def __init__(self, directory: str, embedding_model: str = 'all-mpnet-base-v2',
                 chunk_size: int = 200, chunk_overlap: int = 40, batch_size: int = 32):
        self.directory = directory
        self.model = SentenceTransformer(embedding_model)
        self.text_chunks = []
        self.chunk_sources = []
        self.index = None
        self.embeddings = None
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.batch_size = batch_size
        self.index_path = os.path.join(directory, 'faiss.index')
        self.chunks_path = os.path.join(directory, 'chunks.pkl')
        self.embeddings_path = os.path.join(directory, 'embeddings.npy')
        self._load_or_build()

    def _extract_text_chunks(self, filepath: str) -> list:
        ext = os.path.splitext(filepath)[1].lower()
        if ext == '.pdf':
            try:
                reader = PdfReader(filepath)
                full_text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
            except Exception:
                return []
        elif ext == '.docx':
            try:
                doc = Document(filepath)
                full_text = " ".join([para.text for para in doc.paragraphs if para.text.strip()])
            except Exception:
                return []
        else:
            return []
        words = full_text.split()
        chunks = []

        i = 0
        while i < len(words):
            chunk_words = words[i:i+self.chunk_size]
            if chunk_words:
                chunk_text = " ".join(chunk_words)
                chunk_id = f"chunk_{i//self.chunk_size}"
                chunks.append({
                    "text": chunk_text,
                    "source": os.path.basename(filepath),
                    "chunk_id": chunk_id
                })
            i += self.chunk_size - self.chunk_overlap
        return chunks

    def _load_or_build(self):

        if os.path.exists(self.chunks_path) and os.path.exists(self.index_path) and os.path.exists(self.embeddings_path):
            with open(self.chunks_path, 'rb') as f:
                self.text_chunks = pickle.load(f)
            self.embeddings = np.load(self.embeddings_path)
            dim = self.embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dim)
            self.index.add(np.array(self.embeddings, dtype=np.float32))
            return

        files = [os.path.join(self.directory, f) for f in os.listdir(self.directory)
                 if f.endswith('.pdf') or f.endswith('.docx')]
        chunks = []

        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_file = {executor.submit(self._extract_text_chunks, f): f for f in files}
            for future in as_completed(future_to_file):
                result = future.result()
                if result:
                    chunks.extend(result)
        self.text_chunks = chunks

        with open(self.chunks_path, 'wb') as f:
            pickle.dump(self.text_chunks, f)


        texts = [chunk["text"] for chunk in self.text_chunks]
        all_embeddings = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i+self.batch_size]
            batch_emb = self.model.encode(batch, show_progress_bar=False)
            all_embeddings.append(batch_emb)
        self.embeddings = np.vstack(all_embeddings)
        np.save(self.embeddings_path, self.embeddings)
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(self.embeddings, dtype=np.float32))
        faiss.write_index(self.index, self.index_path)

    def search(self, query: str, top_k: int = 5) -> list:

        query_vec = self.model.encode([query])
        D, I = self.index.search(np.array(query_vec, dtype=np.float32), top_k)
        results = [self.text_chunks[i] for i in I[0]]
        return results
