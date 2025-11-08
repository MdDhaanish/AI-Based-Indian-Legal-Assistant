
import os
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib

# Using the preprocessing module
try:
    from text_preprocessing import preprocess_text
    def preprocess_for_model(text):
        tokens = preprocess_text(text)   # returns list
        return " ".join(tokens)
except Exception:
    import re
    def preprocess_for_model(text):
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

DATA_PATH = os.path.join("data", "question_labels.csv")
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)
MODEL_PATH = os.path.join(MODEL_DIR, "question_classifier.joblib")

def load_data(path):
    df = pd.read_csv(path)
    df = df.dropna(subset=["query", "label"])
    df['text'] = df['query'].astype(str).apply(preprocess_for_model)
    return df

def train_and_save():
    print("Loading data...")
    df = load_data(DATA_PATH)
    X = df['text'].values
    y = df['label'].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    # Build pipeline: TF-IDF -> Logistic Regression
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1,2), max_df=0.85, min_df=1)),
        ("clf", LogisticRegression(max_iter=1000, solver='liblinear'))
    ])

    print("Training classifier...")
    pipeline.fit(X_train, y_train)

    # Evaluate
    print("Evaluating on test set...")
    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {acc:.4f}\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # Cross-validation (optional)
    print("Cross-validation (5-fold) accuracy:", cross_val_score(pipeline, X, y, cv=2).mean())

    # Confusion matrix (optional)
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Save model
    joblib.dump(pipeline, MODEL_PATH)
    print(f"\nSaved trained model to: {MODEL_PATH}")

if __name__ == "__main__":
    train_and_save()
