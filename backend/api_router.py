from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import google.generativeai as genai
from backend.query_handler import route_query
from backend.google_oauth import router as google_oauth_router

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

# Include Google OAuth router
app.include_router(google_oauth_router)


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




