from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import json
import google.generativeai as genai
from backend.query_handler import route_query
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
#from backend.google_oauth import router as google_oauth_router
from backend.auth_router import router as auth_router



# -----------------------------------------------------------
# Initialize FastAPI
# -----------------------------------------------------------
app = FastAPI(title="Legal RAG Assistant API")

# -----------------------------------------------------------
# CORS FOR STREAMLIT + HTML FRONTEND
# -----------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------------------------
# Include Google OAuth router

app.include_router(auth_router)
# -----------------------------------------------------------
# Gemini Model Configuration
# -----------------------------------------------------------



# Load .env file
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY is missing! Add it to your .env file.")

genai.configure(api_key=GOOGLE_API_KEY)


# Choose model
model = genai.GenerativeModel("gemini-2.0-flash")



# -----------------------------------------------------------
# Feedback Model
# -----------------------------------------------------------
class Feedback(BaseModel):
    user: Optional[str]
    question: str
    rating: str   # "up" or "down"

@app.post("/feedback")
async def submit_feedback(payload: Feedback):
    """
    Save user feedback (helpful / not helpful)
    """
    feedback_data = {
        "user": payload.user or "anonymous",
        "question": payload.question,
        "rating": payload.rating,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Save to file (simple + safe)
    feedback_file = "feedback.json"

    if os.path.exists(feedback_file):
        with open(feedback_file, "r", encoding="utf-8") as f:
            feedback_list = json.load(f)
    else:
        feedback_list = []

    feedback_list.append(feedback_data)

    with open(feedback_file, "w", encoding="utf-8") as f:
        json.dump(feedback_list, f, indent=2)

    return {"success": True}

# -----------------------------------------------------------
# Query Model
# -----------------------------------------------------------
class Query(BaseModel):
    question: str



# -----------------------------------------------------------
# CHAT ENDPOINT
# -----------------------------------------------------------
@app.post("/chat")
async def chat_endpoint(payload: Query):
    """
    Accepts a user question and returns:
    - Simple Explanation (plain language)
    - Legal Explanation (formal IPC / CrPC / Acts)
    """

    user_q = payload.question.strip()

    if not user_q:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # -----------------------------------------------------------
    # AI Prompt
    # -----------------------------------------------------------
    ai_prompt = f"""
    You are an expert Indian Legal Assistant.

    For the following user query, respond in EXACTLY TWO SECTIONS:

    **Simple Explanation:**  
    - Explain clearly in simple, beginner-friendly English  
    - Avoid legal jargon  
    - Keep it under 5 sentences  

    **Legal Explanation:**  
    - Provide the detailed legal answer  
    - Cite the relevant IPC / CrPC / Evidence Act / Constitution sections  
    - Use accurate legal terminology  
    - Keep it factual and concise  

    User query: "{user_q}"
    """

    # -----------------------------------------------------------
    # Call Gemini Model
    # -----------------------------------------------------------
    try:
        result = model.generate_content(ai_prompt)
        answer_text = result.text

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Model Error: {str(e)}")

    # -----------------------------------------------------------
    # Extract Two Sections
    # -----------------------------------------------------------
    simple = "Not available."
    legal = "Not available."

    if "**Simple Explanation:**" in answer_text:
        try:
            parts = answer_text.split("**Legal Explanation:**")
            simple = parts[0].replace("**Simple Explanation:**", "").strip()
            legal = parts[1].strip()
        except:
            simple = answer_text
            legal = "Formatting error in model output."
    else:
        simple = answer_text
        legal = "Model did not follow format."

    # -----------------------------------------------------------
    # Final JSON Response
    # -----------------------------------------------------------
    return {
        "simple": simple,
        "legal": legal
    }


# -----------------------------------------------------------
# HOME TEST ENDPOINT
# -----------------------------------------------------------
@app.get("/")
def home():
    return {"message": "Legal RAG Backend Running ✅"}




