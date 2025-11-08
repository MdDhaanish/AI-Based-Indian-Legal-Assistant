import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import re

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True) 
nltk.download('stopwords', quiet=True)

# Load SpaCy English model
nlp = spacy.load("en_core_web_sm")

# English stopwords
stop_words = set(stopwords.words('english'))

# --- Text Preprocessing Pipeline ---

def clean_text(text):
    """Remove punctuation, numbers, and convert to lowercase."""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)  # keep only alphabets
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize_text(text):
    """Tokenize text into words."""
    return word_tokenize(text)

def remove_stopwords(tokens):
    """Remove stopwords from list of tokens."""
    return [word for word in tokens if word not in stop_words]

def lemmatize_tokens(tokens):
    """Lemmatize tokens using SpaCy."""
    doc = nlp(" ".join(tokens))
    return [token.lemma_ for token in doc]

def preprocess_text(text):
    """Full pipeline: clean → tokenize → remove stopwords → lemmatize."""
    cleaned = clean_text(text)
    tokens = tokenize_text(cleaned)
    no_stop = remove_stopwords(tokens)
    lemmatized = lemmatize_tokens(no_stop)
    return lemmatized

# --- Demo ---

if __name__ == "__main__":
    sample_text = "What is the punishment for theft under the Indian Penal Code?"
    print("🔹 Original:", sample_text)
    result = preprocess_text(sample_text)
    print("✅ Preprocessed:", result)
