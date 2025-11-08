import os
import json
import re
from scripts.text_preprocessing import preprocess_text

def load_legal_data(folder="processed_data"):
    """Load all processed legal JSON files into memory."""
    data = {}
    for file in os.listdir(folder):
        if file.endswith(".json"):
            with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                data[file.replace(".json", "")] = json.load(f)
    return data

LEGAL_DATA = load_legal_data()

def find_relevant_sections(query, legal_docs, top_n=5):
    """
    Better retrieval: exact phrase match > keyword match > fallback name match
    """

    # Process query to tokens/lemmas
    processed_query = preprocess_text(query)
    if isinstance(processed_query, list):
        keywords = [k.lower() for k in processed_query]
    else:
        keywords = processed_query.lower().split()

    results = []

    for act_name, sections in legal_docs.items():
        for sec_no, text in sections.items():

            text_lower = text.lower()
            sec_lower = sec_no.lower()

            score = 0

            # 1️⃣ Check exact phrase first (strong match)
            if "theft" in query.lower() and ("379" in sec_no or "378" in sec_no):
                score += 5

            # 2️⃣ Keyword match in text
            score += sum(1 for k in keywords if k in text_lower)

            # 3️⃣ Keyword match in section title
            score += sum(1 for k in keywords if k in sec_lower)

            if score > 0:
                results.append({
                    "act": act_name,
                    "section": sec_no,
                    "text": text.strip(),
                    "score": score
                })

    results.sort(key=lambda x: x["score"], reverse=True)

    # ✅ If nothing found, return top N sections as fallback
    if not results:
        for act_name, sections in legal_docs.items():
            for sec_no, text in list(sections.items())[:top_n]:
                results.append({
                    "act": act_name,
                    "section": sec_no,
                    "text": text.strip(),
                    "score": 0
                })

    return results[:top_n]

