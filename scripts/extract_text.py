import os
import pdfplumber
from PyPDF2 import PdfReader

# Folder paths
DATA_DIR = "data"
OUTPUT_DIR = "extracted_text"

# Create output directory if not exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_with_pdfplumber(pdf_path):
    """Extracts clean text from PDF using pdfplumber."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_with_pypdf2(pdf_path):
    """Fallback extraction using PyPDF2."""
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text


def clean_legal_text(text):
    """Basic cleaning to remove unwanted characters or spacing."""
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    cleaned = "\n".join(lines)
    return cleaned


def extract_all_pdfs():
    """Extract text from all PDFs in the data folder."""
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(DATA_DIR, filename)
            txt_filename = filename.replace(".pdf", ".txt")
            txt_output_path = os.path.join(OUTPUT_DIR, txt_filename)

            print(f"Extracting text from {filename}...")

            # Try pdfplumber first
            try:
                text = extract_with_pdfplumber(pdf_path)
                if not text.strip():
                    raise ValueError("Empty output from pdfplumber, retrying with PyPDF2...")
            except Exception as e:
                print(f"⚠️ pdfplumber failed for {filename}: {e}")
                text = extract_with_pypdf2(pdf_path)

            cleaned_text = clean_legal_text(text)

            with open(txt_output_path, "w", encoding="utf-8") as f:
                f.write(cleaned_text)

            print(f"✅ Saved extracted text to: {txt_output_path}\n")


if __name__ == "__main__":
    extract_all_pdfs()
