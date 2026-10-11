# Service xử lý file upload (kiểm tra định dạng, dung lượng, đọc nội dung)
from fastapi import UploadFile
from schemas.document import DocumentCreate


class FileService:
    allow_extension = (".txt",".md")
    MAX_FILE_SIZE = 2*1024*1024

    @classmethod
    async def process_uploaded_file(cls, file: UploadFile) -> DocumentCreate:
        filename = (file.filename or "").lower()
        if(not filename.endswith(cls.allow_extension)):
            raise ValueError(f"only support file end with {cls.allow_extension}")
        content_byte = await file.read()

        if len(content_byte) > cls.MAX_FILE_SIZE or len(content_byte) <= 0:
            raise ValueError(f"file must not be 0 byte or bigger then {str(cls.MAX_FILE_SIZE)}")

        try:
            text_content = content_byte.decode("utf-8")
        except UnicodeDecodeError:
            raise ValueError("file must be utf-8")

        await file.close()

        return DocumentCreate(
            filename= file.filename,
            file_size= len(content_byte),
            content= text_content
        )