from backend.llm_router import generate_answer

def simplify_answer(user_query, legal_answer, sections):
    # Build context again (in case the model needs it)
    context = "\n\n".join([f"{s['section']}: {s['text']}" for s in sections])

    simplification_prompt = f"""
You are a legal explainer for normal Indian citizens.

User Question:
{user_query}

Formal Legal Answer:
{legal_answer}

Simplify this answer:
- Use simple everyday language
- Keep it short (2–3 lines)
- Still mention section number
- DO NOT include the full law or long examples
- Do not add extra legal points
- Focus on the main idea and return it in english.

Return only the simplified answer:
"""


    refined = generate_answer(simplification_prompt, sections)
    return refined
