// src/services/chatService.ts
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export interface ChatResponse {
  simple?: string;
  legal?: string;
  // keep other fields flexible
  [k: string]: any;
}

export async function sendQuestion(question: string) : Promise<ChatResponse> {
  const res = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Backend error: ${res.status} ${text}`);
  }

  const data = await res.json();
  return data as ChatResponse;
}

export async function sendFeedback(payload: { user: string | null; question: string; rating: "up"|"down"; details?: string }) {
  // optional endpoint. Create /feedback in backend to accept this.
  await fetch(`${API_URL}/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}
