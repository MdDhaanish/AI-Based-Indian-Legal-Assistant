# ⚖️ AI-Based Indian Legal Assistant (LegalAI)

LegalAI is a **full-stack AI-powered Indian legal assistant** that answers legal questions related to **IPC, CrPC, and Indian laws**.  
It provides both **simple, citizen-friendly explanations** and **formal legal explanations** using **Google Gemini AI**.

The system uses a **React frontend**, **FastAPI backend**, **Google authentication**, and **JWT-based security**.

---

## 🚀 Key Features

✅ Ask Indian legal questions in natural language  
✅ Simple explanation (easy-to-understand)  
✅ Formal legal explanation (lawyer-style)  
✅ Google Login (One Tap) + Email/Password login  
✅ Secure JWT-based authentication  
✅ YAML-based credential storage  
✅ Feedback system (Helpful / Not Helpful)  
✅ FastAPI backend + Gemini AI  
✅ Modern React UI  

---

## 🏗️ Architecture Overview

```

React 
|
|  → Auth (Google / Email)
|  → Chat Queries
v
FastAPI Backend
|
|  → JWT Authentication
|  → Feedback API
|  → Gemini AI
v
Google Gemini API

```

---

## 🛠 Tech Stack

### **Frontend**
| Tech | Purpose |
|---|---|
| React | UI |
| React Router | Routing |
| Shadcn UI | Components |
| Axios / Fetch | API calls |

---

### **Backend**
| Tech | Purpose |
|---|---|
| FastAPI | REST API |
| Uvicorn | ASGI server |
| Pydantic | Request validation |
| PyJWT | JWT authentication |
| Bcrypt | Password hashing |
| PyYAML | YAML-based user storage |
| python-dotenv | Environment variables |

---

### **AI**
| Tech | Purpose |
|---|---|
| Google Gemini 2.0 Flash | Legal response generation |

---

## 📂 Main Project Structure

```

project/
│
├── backend/
│   ├── api_router.py        # FastAPI app (chat + feedback)
│   ├── auth_router.py       # Login / Signup / Google auth
│   ├── google_auth.py       # Google token verification
│   ├── credentials/
│   │   └── auth_config.yaml # Authorized user storage
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Auth.tsx     # Login / Signup / Google auth
│   │   │   └── Chat.tsx     # Chat UI + feedback
│   │   ├── chatService.ts  # API calls
│   │   └── App.tsx
│
├── feedback.json            # User feedback storage
├── requirements.txt
├── README.md

```

---

## 🔐 Authentication System

### ✅ Supported Methods
- Google Login (One Tap)
- Email + Password Signup/Login

### ✅ Auth Details
- JWT issued by backend
- Token stored in `localStorage`
- Protected `/chat` route
- Users stored in `auth_config.yaml`

---

## 🧪 Feedback System

After every AI response, users can submit:
- 👍 Helpful
- 👎 Not Helpful

Feedback is stored in:
```

feedback.json

````

Example:
```json
{
  "user": "user@email.com",
  "question": "What is IPC section 420?",
  "rating": "up",
  "timestamp": "2025-11-27T10:20:00Z"
}
````

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone <your-repo-url>
cd project
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

---

### 3️⃣ Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Environment Variables

#### Backend `.env`

```env
GOOGLE_API_KEY=your_gemini_api_key
GOOGLE_OAUTH_CLIENT_ID=your_google_client_id.apps.googleusercontent.com
AUTH_JWT_SECRET=your_secret_key
```

#### Frontend `.env`

```env
VITE_API_URL=http://localhost:8000
VITE_GOOGLE_CLIENT_ID=your_google_client_id.apps.googleusercontent.com
```

---

### 5️⃣ Run Backend

```bash
uvicorn backend.api_router:app --reload
```

Backend runs at:

```
http://localhost:8000
```

---

### 6️⃣ Run Frontend

```bash
npm install
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

## 💬 Example Usage

**User asks**

```
What is the punishment for theft under IPC?
```

**AI responds**
✅ Simple Explanation
✅ Formal Legal Explanation
✅ Relevant IPC sections

---

## 🔒 Security Notes

* Passwords are hashed using `bcrypt`
* JWT is validated on protected routes
* Google ID tokens are verified server-side
* YAML-based auth is suitable for small-scale apps (can migrate to DB later)

---

## 🏁 Conclusion

LegalAI demonstrates a **modern, secure, AI-powered legal assistant** built with:

* React frontend
* FastAPI backend
* Google authentication
* Gemini AI

Ideal for:

* Legal-tech projects
* AI-based law assistants
* Academic / portfolio use

---



