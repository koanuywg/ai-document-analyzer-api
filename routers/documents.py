# Router cho các endpoint xử lý tài liệu (/documents/upload, /documents/, /documents/{id}/ask)
from fastapi import Query, Path, Depends, HTTPException, status, APIRouter, UploadFile, File, BackgroundTasks
from typing import Optional
from schemas.document import DocumentCreate, DocumentResponse, AskQuestionRequest, AskQuestionResponse
from services.file_service import FileService
from services.document_service import DocumentService
from dependencies.auth import get_current_user
from core.supabase import supabase

router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...,description="Chọn file văn bản định dạng .txt hoặc .md"),
    current_user = Depends(get_current_user),
    background_task: BackgroundTasks = BackgroundTasks()
):
    try:
        doc_data = await FileService.process_uploaded_file(file)
        save_doc = DocumentService.create_document(doc_data, current_user.id)
        background_task.add_task(
            DocumentService.process_ai_in_background,
            doc_id=save_doc["id"],
            content=save_doc["content"]
        )
        return save_doc
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model = list[DocumentResponse])
def get_documents(
    current_user = Depends(get_current_user),
    limit: Optional[int] = Query(10, gt=0)
):
    try:
        docs_list = DocumentService.get_documents(current_user.id, limit)
        return docs_list
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{document_id}",response_model = DocumentResponse)
def get_document(
    document_id: int = Path(..., gt=0),
    current_user = Depends(get_current_user)
):
    try:
        doc = DocumentService.get_document(current_user.id,document_id)
        return doc
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{document_id}", status_code=status.HTTP_200_OK)
def delete_document(
    document_id: int = Path(..., gt=0),
    current_user = Depends(get_current_user)
):
    try:
        response = DocumentService.delete_document(current_user.id, document_id)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/{document_id}/ask", response_model=AskQuestionResponse)
def ask_document(
    document_id: int = Path(..., gt=0),
    payload: AskQuestionRequest = ...,
    current_user = Depends(get_current_user)
):
    try:
        # Gọi hàm ask_document của DocumentService để lấy câu trả lời
        answer = DocumentService.ask_document(
            user_id=current_user.id,
            doc_id=document_id,
            question=payload.question
        )
        
        # Trả về đúng schema AskQuestionResponse
        return {
            "id": document_id,
            "question": payload.question,
            "answer": answer
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )