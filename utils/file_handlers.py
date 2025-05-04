import os
import uuid
import logging
import pdfplumber
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError
from docx import Document

# Helper functions first
def _extract_pdf_text(file_path: str) -> str:
    """PDF text extraction helper"""
    print("__ Extracting PDF text from:", file_path)
    try:
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join([page.extract_text() or '' for page in pdf.pages])
            print("_loop1")
            print("__ Extracted text:")
            if text.strip():
                return text.strip()
        
        # Fallback to PyPDF2
        with open(file_path, 'rb') as f:
            pdf = PdfReader(f)
            text = "\n".join([page.extract_text() or '' for page in pdf.pages])
            print("__ Extracted text (PyPDF2):", text[:100])
            return text.strip()
            
    except PdfReadError:
        raise ValueError("PDF is encrypted or corrupted")
    except Exception as e:
        raise ValueError(f"PDF processing error: {str(e)}")

def _extract_docx_text(file_path: str) -> str:
    """DOCX text extraction helper"""
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs]).strip()
    except Exception as e:
        raise ValueError(f"DOCX processing error: {str(e)}")

# Main functions
def save_uploaded_file(uploaded_file, temp_dir: str) -> str:
    """Save uploaded file with UUID filename"""
    try:
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        file_name = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(temp_dir, file_name)
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        return file_path
        
    except Exception as e:
        logging.error(f"File save error: {str(e)}")
        raise

def extract_cv_text(file_path: str) -> str:
    """Main text extraction function"""
    print("Extracting text from:", file_path)
    try:
        file_ext = os.path.splitext(file_path)[1].lower()
        print("File extension:", file_ext)
        if file_ext == '.pdf':
            print("pdf")
            textpdf = _extract_pdf_text(file_path)
            if textpdf:
                print("loop1")
                return textpdf
            else:
                raise ValueError("No text found in PDF")
        elif file_ext == '.docx':
            print("docx")
            return _extract_docx_text(file_path)
        #raise ValueError(f"Unsupported file type: {file_ext}")
            
    except Exception as e:
        logging.error(f"Extraction failed: {str(e)}")
        raise