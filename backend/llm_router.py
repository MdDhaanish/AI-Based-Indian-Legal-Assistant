import os

# Load model choice
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()

# ---- Import Models ----

# Gemini (Current Default)
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
gem_model = genai.GenerativeModel("gemini-2.5-flash")

# OpenAI (If OPENAI_API_KEY set)
try:
    from openai import OpenAI
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception:
    openai_client = None

# Ollama (if LLM_PROVIDER is "ollama")
import requests

# ---- Unified call ----
def generate_answer(query, sections):
    context = "\n\n".join([f"{s['section']}: {s['text']}" for s in sections])

    prompt = f"""
You are an Indian legal assistant. Answer the question strictly based on the law sections provided.

User Question:
{query}

Relevant IPC/CrPC Sections:
{context}

Instructions for Legal Answer:
- Give a precise legal explanation (10-15 lines)
- Cite section numbers
- Maintain legal tone
- DO NOT include full law text or long illustrations
- Highlight the section numbers
- Focus on the legal aspects only
- Just summarize the key legal idea from the law text
- If law not found in input, say "Not available in dataset"

Now give the legal answer only:
"""


    # Gemini (Default)
    if LLM_PROVIDER == "gemini":
        response = gem_model.generate_content([prompt])
        return response.text.strip()

    # OpenAI GPT
    elif LLM_PROVIDER == "openai" and openai_client:
        r = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return r.choices[0].message.content.strip()

    # Ollama Local
    elif LLM_PROVIDER == "ollama":
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={"model":"mistral", "prompt":prompt}
        )
        return resp.json().get("response", "").strip()

    # Fallback
    return "Model not configured or unavailable."
