from pydantic import BaseModel, Field

class PDFUploadResponse(BaseModel):

    id: str = Field(..., alias="_id", description="PDF id")

    class Config:
        populate_by_name = True
class PDFChatRequest(BaseModel):

    message: str = Field(..., description="Kullanıcıdan gelen mesaj")

class PDFChatResponse(BaseModel):

    response: str = Field(..., description="AI response")
