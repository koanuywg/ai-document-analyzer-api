# Schemas Pydantic cho Đăng ký, Đăng nhập, Token và Thông tin User
from pydantic import Field, BaseModel, EmailStr
from typing import Optional

class UserResponse(BaseModel):
    id: str
    email: str

class TokenResponse(BaseModel):
    id: str
    email: str
    token_key: str
    token_type: str = "bearer"

class UserAuth(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)