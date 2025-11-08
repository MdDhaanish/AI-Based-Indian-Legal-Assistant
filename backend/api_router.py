from fastapi import FastAPI
from pydantic import BaseModel
from backend.query_handler import route_query

app = FastAPI(title="Legal RAG Assistant API")

class Query(BaseModel):
    query: str

@app.post("/chatbot")
def chatbot_flow(inp: Query):
    category, matches, final_answer, simplified = route_query(inp.query)
    #print(">>> Matches:", matches)
    
    return {
        "category": category,
        "sections_used": matches,
        "answer": final_answer,
        "simplified": simplified
    }

@app.get("/")
def home():
    return {"message": "Legal RAG Backend Running ✅"}
