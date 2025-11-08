from backend.llm_router import generate_answer
from backend.llm_refiner import simplify_answer
from backend.nlp_connector import find_relevant_sections, LEGAL_DATA
import joblib, os

MODEL_PATH = "models/question_classifier.joblib"
classifier = joblib.load(MODEL_PATH)

CATEGORY_MAP = {
    "criminal": ["IPC", "CrPC"],
    "civil": ["CivilCode"],
    "constitutional": ["Constitution"]
}

def route_query(query):
    pred = classifier.predict([query])[0]

    # Select only the acts relevant to predicted category
    rel_acts = {act: LEGAL_DATA[act] for act in CATEGORY_MAP[pred] if act in LEGAL_DATA}

    # Retrieve top relevant law sections
    matches = find_relevant_sections(query, rel_acts, top_n=4)

    # Gemini final answer

    final_answer = generate_answer(query, matches)
    simplified = simplify_answer(query, final_answer, matches)


    return pred, matches, final_answer, simplified
