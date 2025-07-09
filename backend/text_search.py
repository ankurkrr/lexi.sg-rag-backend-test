from typing import List

def search_relevant_texts(question: str, legal_texts: List[str]) -> List[str]:
    # Placeholder for a more advanced search algorithm
    relevant_texts = []
    for text in legal_texts:
        if question.lower() in text.lower():
            relevant_texts.append(text)
    return relevant_texts
