import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
import spacy
import os

# Initialize NLP
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nlp = spacy.load("en_core_web_sm")

RAW_QUERY_FILE = "data/user_queries_raw.csv"
CLEANED_QUERY_FILE = "processed_data/user_queries_clean.csv"

# Ensure output folder exists
os.makedirs("processed_data", exist_ok=True)

# --- Helper functions ---

def clean_text(text):
    """Lowercase, remove punctuation, and extra spaces."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def lemmatize_text(text):
    """Use SpaCy to lemmatize text (normalize word forms)."""
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc if not token.is_stop])

def preprocess_query(text):
    """Combine cleaning + lemmatization."""
    cleaned = clean_text(text)
    lemmatized = lemmatize_text(cleaned)
    return lemmatized

def prepare_dataset():
    """Load, clean, preprocess, and save user queries."""
    if not os.path.exists(RAW_QUERY_FILE):
        print(f"❌ Raw query file not found at {RAW_QUERY_FILE}")
        return

    df = pd.read_csv(RAW_QUERY_FILE)

    if 'query' not in df.columns:
        print("❌ CSV must contain a 'query' column.")
        return

    print("🧹 Cleaning and preprocessing user queries...")

    df['cleaned_query'] = df['query'].apply(preprocess_query)

    # Optional: remove duplicates and empty queries
    df.drop_duplicates(subset='cleaned_query', inplace=True)
    df.dropna(subset=['cleaned_query'], inplace=True)

    df.to_csv(CLEANED_QUERY_FILE, index=False)
    print(f"✅ Cleaned queries saved to {CLEANED_QUERY_FILE}")


if __name__ == "__main__":
    prepare_dataset()
