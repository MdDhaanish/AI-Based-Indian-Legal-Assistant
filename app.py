import streamlit as st
import json
import os
import re

# --- Helper Functions ---

def load_all_json(data_folder="processed_data"):
    """Load all processed JSON files into memory."""
    legal_docs = {}
    for file in os.listdir(data_folder):
        if file.endswith(".json"):
            with open(os.path.join(data_folder, file), "r", encoding="utf-8") as f:
                doc_name = file.replace(".json", "")
                legal_docs[doc_name] = json.load(f)
    return legal_docs


def search_legal_sections(query, legal_docs, top_n=3):
    """
    Simple keyword-based search.
    Finds sections containing any query keywords and ranks them by keyword count.
    """
    query = query.lower()
    keywords = re.findall(r'\w+', query)
    results = []

    for act_name, sections in legal_docs.items():
        for sec_no, text in sections.items():
            text_lower = text.lower()
            match_count = sum(1 for kw in keywords if kw in text_lower)
            if match_count > 0:
                results.append({
                    "act": act_name,
                    "section": sec_no,
                    "text": text.strip(),
                    "score": match_count
                })

    # Sort by match score (descending)
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]


# --- Streamlit UI ---

st.set_page_config(page_title="Legal Query Assistant", layout="centered")
st.title("⚖️ Legal Query Assistant")
st.markdown("Ask questions related to Indian laws like IPC, CrPC, and Evidence Act.")

# Load legal data
st.sidebar.header("📚 Data Status")
try:
    legal_docs = load_all_json()
    st.sidebar.success(f"Loaded {len(legal_docs)} legal documents ✅")
except Exception as e:
    st.sidebar.error(f"Error loading documents: {e}")
    legal_docs = {}

# User query input
user_query = st.text_input("Enter your legal query:", placeholder="e.g., punishment for theft under IPC")

if st.button("Search"):
    if not user_query.strip():
        st.warning("Please enter a query.")
    elif not legal_docs:
        st.error("No legal data found. Run text extraction and processing scripts first.")
    else:
        results = search_legal_sections(user_query, legal_docs)

        if results:
            st.subheader("🔍 Relevant Sections Found:")
            for res in results:
                with st.expander(f"{res['act']} — {res['section']}"):
                    st.write(res['text'])
        else:
            st.info("No matching sections found. Try using different keywords.")
