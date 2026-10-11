# Dependency kiểm tra token và xác thực người dùng (get_current_user)
from fastapi import Depends, HTTPException,status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from core.supabase import supabase

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        current_user = supabase.auth.get_user(token)
        if not current_user or not current_user.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="token ko hop le hoac da het han"
            )
        return current_user.user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"ko the xac thuc {str(e)}"
        )