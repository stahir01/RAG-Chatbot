import os
import json
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from backend.app.config import PROJECT_ROOT


class PDFExtraction:
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """
        Extract text from a PDF file using PyPDFLoader.
        """
        try:
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            return [page.page_content for page in documents]
        except Exception as e: 
            raise Exception(f"Error extracting text from PDF: {e}")

    @staticmethod
    def extract_text_from_json(file_path: str) -> str:
        pass

    @staticmethod
    def extract_text_from_voice(file_path: str) -> str:
        pass




if __name__ == "__main__":
    pdf_path = os.path.join(PROJECT_ROOT, "documents", "Guideline_atraumatische_Femurkopfnekrose_2019-09_1-abgelaufen.pdf")

    try:
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"File not found: {pdf_path}")
        
        pdf_extractor = PDFExtraction()
        text = pdf_extractor.extract_text_from_pdf(pdf_path)
        with open("extracted_text.json", "w") as f:
            json.dump(text, f, indent=4)
        print("Text extracted successfully.")
    except FileNotFoundError as e:
        print(e)