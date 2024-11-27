from datetime import datetime
from app.utils.pdf_processor import PDFProcessor
from app.deps import MongoDep, LLMDep
def process_and_save_pdf(file_content: bytes, file_name: str, s3_manager: LLMDep, mongo_manager: MongoDep) -> dict:

    # pdf contetini cikar
    extracted_data = PDFProcessor.extract_text(file_content)

    current_date = datetime.now()
    year = current_date.strftime("%Y")
    month = current_date.strftime("%m")
    s3_key = f"{year}/{month}/{file_name}"
    s3_url = s3_manager.upload_file(file_content, s3_key)

    # Metadata ve content bilgisi
    pdf_data = {
        "filename": file_name,
        "upload_date": current_date.strftime("%Y-%m-%d"),
        "s3_url": s3_url,
        "content": extracted_data["content"],
        "page_count": extracted_data["page_count"]
    }
    # Mongo dbye kaydet
    inserted_id = mongo_manager.add(collection="pdf_data", data=pdf_data)

    return {"_id": str(inserted_id)}


def interact_with_pdf(_id: str, message: str, mongo_manager: MongoDep, llm_service: LLMDep) -> dict:

    # Get pdf data
    pdf_data = mongo_manager.get_by_object_id(collection="pdf_data", _id=_id)
    pdf_content = pdf_data.get("content")

    # Create request
    request = [message, pdf_content]
    response = llm_service.ask(request)
    return {"response": response}
