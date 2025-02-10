import os
import json
from typing import Optional, List
from langchain_community.document_loaders import PyPDFLoader


def load_pdf(pdf_path: str) -> List:
    """
    Loads and extracts document data from a PDF file.

    Args:
        pdf_path (str): The file path to the PDF document.

    Returns:
        List: A list of documents extracted from the PDF.
    """
    loader = PyPDFLoader(file_path=pdf_path)
    documents = loader.load()
    extracted_documents = []

    for pages in documents:
        extracted_documents.append({"text": pages.page_content, "page": pages.metadata["page"]})

    return extracted_documents

def load_json(json_path: str) -> List:
    """
    Loads and extracts document data from a JSON file without using jq.

    Args:
        json_path (str): The file path to the JSON document.

    Returns:
        List: A list of extracted documents.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    extracted_documents = []

    # Extract key sections
    if "abstract" in json_data:
        extracted_documents.append({"text": json_data["abstract"], "page": "JSON"})

    if "key_contributions" in json_data:
        for contribution in json_data["key_contributions"]:
            extracted_documents.append({"text": contribution["description"], "page": "JSON"})

    if "impact" in json_data:
        for impact in json_data["impact"]:
            extracted_documents.append({"text": impact, "page": "JSON"})

    return extracted_documents
