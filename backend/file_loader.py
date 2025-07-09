
import os
import warnings
import logging
from PyPDF2 import PdfReader
from docx import Document

# Suppress warnings and set logging to ERROR
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.ERROR)

def load_legal_files(directory):
    legal_texts = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if filename.endswith('.pdf'):
            legal_texts.extend(extract_text_from_pdf(filepath))
        elif filename.endswith('.docx'):
            legal_texts.extend(extract_text_from_docx(filepath))
    return legal_texts

def extract_text_from_pdf(filepath):
    texts = []
    try:
        reader = PdfReader(filepath)
        for i, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text()
            except Exception as e:
                logging.error(f"Error extracting text from page {i+1} in {filepath}: {e}")
                continue
            if page_text:
                texts.append({
                    "text": page_text.strip(),
                    "source": os.path.basename(filepath),
                    "location": f"page_{i+1}"
                })
    except Exception as e:
        logging.error(f"Error reading PDF {filepath}: {e}")
    return texts

def extract_text_from_docx(filepath):
    texts = []
    try:
        doc = Document(filepath)
        for i, paragraph in enumerate(doc.paragraphs):
            try:
                para_text = paragraph.text.strip()
            except Exception as e:
                logging.error(f"Error extracting text from paragraph {i+1} in {filepath}: {e}")
                continue
            if para_text:
                texts.append({
                    "text": para_text,
                    "source": os.path.basename(filepath),
                    "location": f"paragraph_{i+1}"
                })
    except Exception as e:
        logging.error(f"Error reading DOCX {filepath}: {e}")
    return texts
