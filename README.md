# 🤖 AI Document Analyzer & Assistant API

> **A Production-Ready FastAPI Backend for Intelligent Document Processing & Q&A using OpenAI and Supabase.**

---

## 🌟 Features
- **User Authentication (JWT & Supabase Auth)**: Multi-tenant user isolation using Bearer token authentication.
- **File Upload & Validation**: Secure streaming of `.txt` and `.md` files with MIME type, extension, and size limits.
- **AI Document Summarization**: Automated summarization and key takeaways extraction using **OpenAI GPT-4o-mini**.
- **Asynchronous Background Tasks**: Non-blocking document processing via FastAPI's `BackgroundTasks`.
- **Grounded Q&A (Ask Document)**: Context-aware document questioning with anti-hallucination prompting.
- **Clean Architecture**: Strict separation of concerns (Routers -> Services -> Database).

---

## 🛠️ Tech Stack
- **Framework**: FastAPI (Python 3.11+)
- **Server**: Uvicorn (ASGI)
- **Database & Auth**: Supabase (PostgreSQL)
- **AI / LLM**: OpenAI API (`gpt-4o-mini`)
- **Validation**: Pydantic v2

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd fastapi-python
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables
Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```
Fill in your credentials:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
OPENAI_API_KEY=your_openai_api_key
```

### 4. Run the server
```bash
uvicorn main:app --reload
```
Visit the interactive Swagger API documentation at: **http://127.0.0.1:8000/docs**
