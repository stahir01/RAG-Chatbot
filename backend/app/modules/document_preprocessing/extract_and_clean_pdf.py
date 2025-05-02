import os
import json
import re
from pathlib import Path
from typing import List, Optional, Pattern
from langchain_community.document_loaders import PyPDFLoader
from backend.app.config import PROJECT_ROOT

class PDFExtraction:
    """
    Text extraction processor using various loaders.
    """
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





class CleanText:
    """Advanced text cleaning processor for medical document preprocessing."""
    def __init__(self, text: str):
        self.text = text
        self._default_header_patterns = [
            r'^S3-Leitlinie.*?Langfassung\s+Version vom \d{2}\.\d{2}\.\d{4}.*?\n',
            r'^Seite \d+ von \d+'
        ]
        self._default_footer_patterns = [
            r'\n\d+\s*$',  # Page numbers at end
            r'©.*?$'       # Copyright notices
        ]
        self._medical_special_chars = r'[^\w\s\.,;:\-\(\)\/°]' # Simplified special chars

    def remove_headers_footers(
            self,
            header_patterns: Optional[List[Pattern]] = None,
            footer_patterns: Optional[List[Pattern]] = None) -> 'CleanText':
        """Remove document headers and footers using configurable regex patterns."""
        patterns = header_patterns or self._default_header_patterns
        patterns += footer_patterns or self._default_footer_patterns
        
        for pattern in patterns:
            self.text = re.sub(pattern, '', self.text, flags=re.MULTILINE | re.IGNORECASE)
        return self
    
    def normalize_unicode(self) -> 'CleanText':
        """Convert/handle Unicode characters."""
        self.text = self.text.encode('utf-8', errors='replace').decode('utf-8')
        return self

    def clean_special_characters(
            self,
            custom_pattern: Optional[str] = None) -> 'CleanText':
        """Remove non-standard characters while preserving medical terminology."""
        pattern = custom_pattern or self._medical_special_chars
        self.text = re.sub(pattern, '', self.text)
        return self
    
    def fix_hyphenation(self) -> 'CleanText':
        """Handle medical compound words and hyphenation."""
        # Fix broken compound words
        self.text = re.sub(r'(\w+)- (\w+)', r'\1\2', self.text)  # Core - decompression → Core decompression
        # Normalize hyphen spacing
        self.text = re.sub(r'\s*-\s*', '-', self.text)
        return self
    
    def normalize_whitespace(self) -> 'CleanText':
        """Advanced whitespace normalization."""
        # Preserve paragraph breaks
        self.text = re.sub(r'\n\s*\n', '\n\n', self.text)
        # Remove extra spaces
        self.text = re.sub(r'[ \t]+', ' ', self.text)
        # Clean line breaks
        self.text = re.sub(r'(?<!\n)\n(?!\n)', ' ', self.text)
        return self
    
    def preserve_references(self) -> 'CleanText':
        """Maintain citation markers for medical references."""
        self.text = re.sub(r'\[(\d+)\]', r'REF\1', self.text)  # Preserve [123] citations
        return self
    
    def clean(self) -> str:
        """Execute full cleaning pipeline with medical document optimizations."""
        return (
            self.normalize_unicode()
            .remove_headers_footers()
            .preserve_references()
            .fix_hyphenation()
            .clean_special_characters()
            .normalize_whitespace()
            .text
        )


if __name__ == "__main__":
    pdf_path = os.path.join(PROJECT_ROOT, "documents", "Guideline_atraumatische_Femurkopfnekrose_2019-09_1-abgelaufen.pdf")
    
    pdf_extractor = PDFExtraction()
    raw_text = pdf_extractor.extract_text_from_pdf(pdf_path)
    
    if isinstance(raw_text, list):
        raw_text = "\n".join(raw_text)
        
    cleaner = CleanText(raw_text)
    cleaned_text = cleaner.clean()
    
    print("Original text length:", len(raw_text))
    print("Cleaned text length:", len(cleaned_text))
    
    with open("cleaned_text.json", "w", encoding="utf-8") as f:
        json.dump({"cleaned_text": cleaned_text}, f, ensure_ascii=False, indent=4)