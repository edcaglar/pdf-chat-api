from fastapi import APIRouter, File, UploadFile, HTTPException, status
from app.deps import S3Dep, MongoDep, LLMDep
from app.services import pdf_manager
from app.models.pdf_models import PDFUploadResponse, PDFChatRequest, PDFChatResponse
from app.exceptions import DocumentNotFoundError, InvalidObjectIdError

pdf_router = APIRouter()
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB limit

@pdf_router.post("/pdf",
                 response_model=PDFUploadResponse,
                 status_code=status.HTTP_201_CREATED)
async def upload_pdf(s3_manager: S3Dep,
                     mongo_manager: MongoDep,
                     file: UploadFile):
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail=f"Dosya boyutu {MAX_FILE_SIZE // (1024 * 1024)} MB'ı geçemez.")
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Sadece PDF dosyaları kabul edilir.")

    try:
        # Dosya içeriğini oku
        content = await file.read()

        # PDF işlemleri
        _id = pdf_manager.process_and_save_pdf(content, file.filename, s3_manager, mongo_manager)
        return PDFUploadResponse(**_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hata oluştu: {str(e)}")


@pdf_router.post("/chat/{_id}", response_model=PDFChatResponse)
async def chat_with_pdf(mongo_manager: MongoDep,
                        llm_service: LLMDep,
                        _id: str,
                        request: PDFChatRequest):
    try:
        response_text = pdf_manager.interact_with_pdf(_id, request.message, mongo_manager, llm_service)
        return PDFChatResponse(**response_text)
    except InvalidObjectIdError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DocumentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Beklenmeyen bir hata oluştu: {str(e)}")