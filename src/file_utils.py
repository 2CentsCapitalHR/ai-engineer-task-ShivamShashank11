
import json
import csv
import os
from typing import List, Tuple, Any
from docx import Document

def read_docx(filepath: str) -> Tuple[Document, List[Any], str]:
    """
    Read a .docx and return (Document object, list of paragraphs, full_text).
    Raises RuntimeError on failure.
    """
    try:
        doc = Document(filepath)
        paragraphs = [p for p in doc.paragraphs]
        text = "\n".join(p.text for p in paragraphs if p.text and p.text.strip())
        return doc, paragraphs, text
    except Exception as e:
        raise RuntimeError(f"Error reading DOCX file {filepath}: {e}")

def write_docx(doc: Document, filepath: str) -> None:
    """
    Save a python-docx Document to filepath (creates parent dirs).
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        doc.save(filepath)
    except Exception as e:
        raise RuntimeError(f"Error saving DOCX file {filepath}: {e}")

def read_json(filepath: str):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"Error reading JSON file {filepath}: {e}")

def write_json(data, filepath: str):
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        raise RuntimeError(f"Error writing JSON file {filepath}: {e}")

def read_csv(filepath: str):
    try:
        with open(filepath, newline='', encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except Exception as e:
        raise RuntimeError(f"Error reading CSV file {filepath}: {e}")

def write_csv(data: List[dict], filepath: str, fieldnames: List[str]):
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        raise RuntimeError(f"Error writing CSV file {filepath}: {e}")

# Alias for compatibility with older code
def save_json(data, filepath: str):
    """Alias for write_json to maintain backward compatibility."""
    return write_json(data, filepath)
