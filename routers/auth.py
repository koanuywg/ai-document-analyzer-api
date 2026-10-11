# Router cho các endpoint xác thực (/auth/register, /auth/login, /auth/me)
from fastapi import Depends, Path, APIRouter, HTTPException, status
from schemas.auth import UserAuth, UserResponse, TokenResponse
from core.supabase import supabase
from dependencies.auth import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    payload: UserAuth
):
    try:
        user_response = supabase.auth.sign_up({
            "email": payload.email,
            "password": payload.password
        })

        if not user_response:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ko the tao tai khoan"
            )
        return {"message": "da tao tai khoan thanh cong", "user_id": user_response.user.id}
    except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"ko the dang ky: {str(e)}"
            )

@router.post("/login", response_model=TokenResponse)
def login(
    payload: UserAuth,
):
    try:
        user_response = supabase.auth.sign_in_with_password({
            "email": payload.email,
            "password": payload.password
        })
        if not user_response.session or not user_response:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ko the dang nhap"
            )
        return {
            "id": user_response.user.id,
            "email": user_response.user.email,
            "token_key": user_response.session.access_token,
            "token_type": user_response.session.token_type
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"ko the dang nhap: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
def get_me(
     current_user = Depends(get_current_user)
):
    try:
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="chua dang nhap"
                )
        return {
            "id": current_user.id,
            "email": current_user.email    
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{str(e)}"
        )