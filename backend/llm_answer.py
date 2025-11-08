import os
import google.generativeai as genai

# Read API Key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GEMINI API key missing — set GOOGLE_API_KEY environment variable.")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

def generate_answer_llm(query, sections):
    """Generate a legal answer using Gemini 2.5 Flash & retrieved law sections."""

    # Build context block from retrieved sections
    context = "\n\n".join(
        [f"{s['section']}: {s['text']}" for s in sections]
    )

    prompt = f"""
You are a highly accurate Indian legal assistant.
Use ONLY the law sections supplied to answer.

User Question:
{query}

Relevant Law Sections:
{context}

Rules:
- Cite IPC/CrPC/Constitution sections directly.
- Keep answer factual, concise, and legally correct.
- If answer not in provided text, reply: "Not available in dataset."

Now answer the user's question with section references:
"""
    
    response = model.generate_content([prompt])
    return response.text.strip()
