# ⚖️ AI-Based Indian Legal Reference Assistant

An AI-powered legal assistant that answers legal queries based on **IPC, CrPC, and the Constitution of India**, retrieves relevant sections, and provides:

- ✅ Formal legal answer (lawyer-style)
- ✅ Simple explanation (citizen-friendly)
- ✅ Relevant IPC/CrPC sections

Built using **NLP + RAG + Gemini AI** with a modern **Streamlit UI** and **FastAPI backend**.

---

## 🚀 Features

| Feature                                            | Description                                   |
| -------------------------------------------------- | --------------------------------------------- |
| ✅ Ask legal questions in natural language          | "What is the punishment for theft under IPC?" |
| ✅ Law classification                               | Criminal / Civil / Constitutional             |
| ✅ Searches relevant IPC/CrPC/Constitution sections | Finds & ranks legal sections                  |
| ✅ AI-generated legal answer                        | Accurate legal explanation (formal tone)      |
| ✅ Simplified citizen-friendly answer               | Easy everyday language                        |
| ✅ Modern UI                                        | Streamlit-based interface                     |
| ✅ API backend                                      | FastAPI endpoint `/chatbot`                   |
| ✅ Local JSON law database                          | IPC / CrPC extracted from PDFs                |


---

## 🏗 Tech Stack

### **Frontend**
| Tech       | Purpose                   |
| ---------- | ------------------------- |
| Streamlit  | UI + input/output display |
| Custom CSS | Modern UI styling         |


### **Backend**
| Tech     | Purpose           |
| -------- | ----------------- |
| FastAPI  | REST API backend  |
| Python   | Core logic        |
| Requests | API call handling |


### **AI / NLP**
| Model / Library         | Purpose                                |
| ----------------------- | -------------------------------------- |
| Google Gemini 2.5 Flash | Answer generation + simplification     |
| NLTK / SpaCy            | Tokenization, stopwords, lemmatization |
| Custom RAG logic        | Retrieve IPC/CrPC & rank sections      |


### **Data Processing**
| Tool       | Purpose                   |
| ---------- | ------------------------- |
| pdfplumber | Extract text from IPC PDF |
| Regex      | Clean & split sections    |
| JSON store | Save IPC/CrPC law text    |


---

## 📂 Project Structure

```

project/
│── app.py                     # Streamlit UI
│── backend/
│   ├── api_router.py          # FastAPI API endpoints
│   ├── query_handler.py       # NLP + retrieval + LLM pipeline
│   ├── llm_router.py          # Selects AI model (Gemini / others)
│   ├── llm_refiner.py         # Generates simplified explanation
│   └── nlp_connector.py       # Preprocessing + section matching
│── processed_data/
│   ├── IPC.json               # Extracted IPC sections
│   └── CrPC.json              # Extracted CrPC sections
│── data/
│   └── IPC.pdf                # Raw PDF (input)
│── extract_ipc.py             # PDF → JSON converter
│── requirements.txt
│── README.md

````

---

## 🛠 Setup Instructions

### 1️⃣ Clone Repo
```bash
git clone <repo-url>
cd project
````

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Add API Key

```
setx GOOGLE_API_KEY "YOUR_GEMINI_KEY"   # Windows
export GOOGLE_API_KEY="YOUR_GEMINI_KEY" # macOS/Linux
```

### 5️⃣ Run Backend (FastAPI)

```bash
uvicorn backend.api_router:app --reload
```

### 6️⃣ Run Frontend (Streamlit)

```bash
streamlit run app.py
```

---

## 🎯 Usage Example

**User Input**

```
Punishment for theft under IPC
```

**Output**
✅ Legal Answer (Section-cited)
✅ Simplified Explanation
✅ IPC Section 378 & 379 displayed

---

## 📊 Dataset

* IPC text extracted from official Government PDF
* Processed into structured JSON format
* Includes section number + legal text

---

## 🧪 Testing

Functional tests included for:

| Test               | Expected        |
| ------------------ | --------------- |
| Theft IPC query    | Section 378/379 |
| Fundamental rights | Article 14-32   |
| FIR process        | CrPC 154        |

---

## 📌 Future Enhancements

| Planned Feature             | Purpose                |
| --------------------------- | ---------------------- |
| ChromaDB / FAISS RAG        | Semantic law search    |
| Full Court Judgement search | Case law support       |
| Hindi / Hinglish output     | Public-friendly access |
| Cloud deployment            | Public web access      |
| Upload case PDF             | Custom legal analysis  |

---

## 🏁 Conclusion

This project demonstrates a fully functional **legal RAG assistant** capable of retrieving Indian law sections, providing accurate responses, and simplifying legal language with AI.

Designed for:

* Law students
* Citizens seeking legal understanding
* Legal tech innovation projects

---

