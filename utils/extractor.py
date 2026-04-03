import pdfplumber
import docx2txt
import pytesseract
from PIL import Image
import os

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    try:
        if ext == '.pdf':
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        elif ext == '.docx':
            text = docx2txt.process(file_path)
        elif ext == '.txt':
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        elif ext in ['.png', '.jpg', '.jpeg']:
            # Tesseract OCR setup (Might require manual config on windows, add the below line if needed)
            # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img)
        else:
            text = "Unsupported file format."
    except Exception as e:
        print(f"Error extracting text from {file_path}: {str(e)}")
    
    return text.strip()
