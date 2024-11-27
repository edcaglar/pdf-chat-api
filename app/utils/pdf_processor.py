import mimetypes
import pymupdf  # PyMuPDF

class PDFProcessor:
    @staticmethod
    def extract_text(file_content: bytes) -> dict:
        pdf_document = pymupdf.open(stream=file_content, filetype="pdf")
        text_content = ""
        for page in pdf_document:
            text_content += page.get_text()

        return {
            "content": text_content.strip(),
            "page_count": len(pdf_document)
        }
