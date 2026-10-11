# Schemas Pydantic cho Tài liệu (Document), Câu hỏi (Ask), Phân tích AI
from pydantic import Field, BaseModel
from typing import Optional
from datetime import date, datetime

class DocumentResponse(BaseModel):
    id: int
    user_id: str
    status: str = "pending"
    created_at: Optional[datetime] = None
    filename: str
    file_size: int
    content: str
    summary: Optional[str] = None
    key_takeaways: Optional[list[str]] = None

class DocumentCreate(BaseModel):
    filename: str = Field(..., min_length=1)
    file_size: int = Field(..., gt=0)
    content: str = Field(..., min_length=1)

class AskQuestionRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=500)

class AskQuestionResponse(BaseModel):
    id: int
    question: str
    answer: str