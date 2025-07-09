# RAG Lexi

A Retrieval-Augmented Generation (RAG) system for answering questions using your own PDF/DOCX documents, powered by HuggingFace LLMs.

---

## Setup Instructions

1. **Clone the repository**

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Download or place your PDF/DOCX files**

   - Place your files in the directory you want to use for document search (e.g., `pdfs/` or a custom folder).
   - Update the path in `backend/main.py` and `backend/vector_store.py` if you use a different folder.

4. **Obtain a HuggingFace Inference Token**

   - Go to [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
   - Click "New token" (choose `read` access)
   - Copy the token (starts with `hf_...`)

5. **Create a `.env` file in the project root**

   Example:
   ```env
   HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

## How to Test the API

1. **Start the backend**

   ```bash
   uvicorn backend.main:app --reload --port 8080
   ```

2. **(Optional) Start the frontend**

   ```bash
   cd frontend
   python app.py
   ```
   - Visit [http://localhost:5000](http://localhost:5000) for the web UI.

3. **Test the API directly**

   Example using `curl`:
   ```bash
   curl -X POST "http://127.0.0.1:8080/query" -H "Content-Type: application/json" -d '{"query": "Is an insurance company liable to pay compensation if a transport vehicle involved in an accident was being used without a valid permit?"}'
   ```

---

## Example Input/Output

**Input:**
```json
{
  "query": "Is an insurance company liable to pay compensation if a transport vehicle involved in an accident was being used without a valid permit?"
}
```

**Output:**
```json
{
  "answer": "No. According to the context, without a permit is considered an infraction and the insurer is not liable. The case of Lakhmi Chand v. Reliance General Insurance (2016) 3 SCC 100 mentioned in the context clarifies that in order to avoid liability, the insurer must establish that there was a breach on the part of the insured. Additionally, the context states that there is a distinction to be made between 'route permit' and 'permit' in the context of Section 149 of the Act, and using the vehicle without a valid permit can be a breach of a specific condition of the policy.",
  "citations": [
    {
      "text": "without a permit is an infraction and insurer is not liable. 18. In Lakhmi Chand v. Reliance General Insurance, (2016) 3 SCC 100, the Court was concerned with an order passed by the National Consumer Disputes Redressal Commission (NCDRC) that had declined the relief to the petitioner therein. The insurer in the said case had taken the plea that the complainant had violated the terms and conditions of the policy, for five passengers were travelling in the goods carrying vehicle at the time of the accident, whereas the permitted seating capacity of the motor vehicle of the appellant was only 1 + 1. The two-Judge Bench referred to Oriental Insurance Co. Ltd. v. Meena Variyal and others, (2007) 5 SCC 428 and expressed the view that in order to avoid liability, the insurer must establish that there was breach on the part of the insured. 19. The obtaining fact situation is sought to be equated with the factual score in the said case. In this regard, it is useful to refer to the Bench decision in HDFC Bank Limited v. Reshma and others, (2015) 3 SCC 679. The issue that arose before the Court was whether the financier was liable",
      "source": "Amrit Paul Singh v. TATA AIG (SC NO ROUTE Permit insurance Co. Recover from Owner).docx"
    },
    { "text": "...", "source": "..." },
    { "text": "...", "source": "..." }
  ]
}
```

---

## Notes
- **PDF/DOCX file location:**
  - Place your files in the folder specified in `main.py` (e.g., `pdfs/`).
  - You can change this path as needed.
- **HF_TOKEN:**
  - Your HuggingFace token must be set in `.env` as `HF_TOKEN=...`.
  - Never share your token publicly.

---

For any issues, please check your `.env`, document folder path, and HuggingFace token permissions.
