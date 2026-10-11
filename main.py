from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, documents

app = FastAPI(
    title="AI Document Analyzer API",
    description="Hệ thống Backend Quản lý & Phân tích Tài liệu Tự động bằng AI",
    version="1.0.0"
)
app.include_router(auth.router)
app.include_router(documents.router)

# Cấu hình CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "project": "AI Document Analyzer API",
        "status": "Online",
        "docs_url": "/docs"
    }
