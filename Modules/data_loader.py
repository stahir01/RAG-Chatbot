import os
import json
from typing import Optional, List
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import  JSONLoader


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
    Loads and extracts document data from a Json file.

    Args:
        pdf_path (str): The file path to the Json document.

    Returns:
        List: A list of documents extracted from the Json.
    """

    loader = JSONLoader(file_path=json_path)
    json_doc = loader.load()

    extracted_documents = []

    for pages in json_doc:
        extracted_documents.append({"text": pages.page_content, "page": pages.metadata["page"]})

    return extracted_documents


