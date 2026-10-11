# Service xử lý logic nghiệp vụ và tương tác Database bảng documents
from schemas.document import DocumentCreate
from core.supabase import supabase
from fastapi import HTTPException, status
from services.ai_service import call_openai


class DocumentService:
    @classmethod
    def create_document(cls, doc_data: DocumentCreate, user_id: str):
        try:
            response = supabase.table("documents").insert({
                "user_id": user_id,
                "filename": doc_data.filename,
                "file_size": doc_data.file_size,
                "content": doc_data.content,
                "status": "pending"
            }).execute()
            if not response.data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="khong the tao doc"
                )
            
            return response.data[0]
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    @classmethod
    def update_ai_result(cls, doc_id: int, result: dict):
        try:
            response = supabase.table("documents").update({
                "summary": result["summary"],
                "key_takeaways": result["key_takeaways"],
                "status": "completed"
            }).eq("id", doc_id).execute()
            if not response.data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="ko update dc doc"
                )
            return response.data[0]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    @classmethod
    def process_ai_in_background(cls, doc_id: int, content: str,call_type:str = "init",ques_in: str=""):
        ai_data = call_openai(content= content, type=call_type,ques=ques_in)
        if call_type=="init":
            cls.update_ai_result(doc_id, ai_data)

    @classmethod
    def ask_document(cls, user_id: str, doc_id: int, question: str) -> str:
        # 1. Lấy tài liệu từ DB (vừa lấy content vừa kiểm tra quyền sở hữu)
        doc = cls.get_document(user_id=user_id, doc_id=doc_id)
        
        # 2. Gọi OpenAI trả lời
        answer = call_openai(content=doc["content"], type="ask", ques=question)
        return answer

  

    @classmethod
    def get_documents(cls, user_id, limit):
        try:
            response = supabase.table("documents").select("*").eq("user_id", user_id).limit(limit).execute()
            return response.data
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    @classmethod
    def get_document(cls, user_id, doc_id):
        try:
            response = supabase.table("documents").select("*").eq("id", doc_id).eq("user_id", user_id).execute()
            if not response.data:
                raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="ko lay dc document"
                    )
            return response.data[0]
        except HTTPException: raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @classmethod
    def delete_document(cls, user_id, doc_id):
        try:
            response = supabase.table("documents").delete().eq("id", doc_id).eq("user_id", user_id).execute()
            if not response.data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="ko the xoa duoc doc"
                )
            return {"message": "da xoa thanh cong"}
        except HTTPException: raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )