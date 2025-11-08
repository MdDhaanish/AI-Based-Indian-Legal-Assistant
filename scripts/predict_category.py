
import joblib
import os
import sys

MODEL_PATH = os.path.join("models", "question_classifier.joblib")

if not os.path.exists(MODEL_PATH):
    print("Model not found. Train it first with scripts/train_classifier.py")
    sys.exit(1)

pipeline = joblib.load(MODEL_PATH)

def predict(query):
    pred = pipeline.predict([query])[0]
    proba = pipeline.predict_proba([query])[0]
    labels = pipeline.classes_
    probs = dict(zip(labels, proba))
    return pred, probs

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/predict_category.py \"your question here\"")
        sys.exit(0)
    q = sys.argv[1]
    label, probs = predict(q)
    print(f"Query: {q}")
    print(f"Predicted label: {label}")
    print("Probabilities:", probs)
