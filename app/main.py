from fastapi import FastAPI
from app.routes.pdf import pdf_router

app = FastAPI(
    title="PDF Chat API",
    description="PDF dosyalarını işleyip kullanıcılarla etkileşime geçmenizi sağlayan bir API",
    version="1.0.0"
)


app.include_router(pdf_router, prefix="/v1", tags=["PDF Operations"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the PDF Chat API"}
