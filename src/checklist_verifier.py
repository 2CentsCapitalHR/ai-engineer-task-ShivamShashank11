import os
from typing import List, Dict

# Checklists for processes
CHECKLISTS = {
    "Company Incorporation": [
        "Articles of Association",
        "Memorandum of Association",
        "Incorporation Application Form",
        "UBO Declaration Form",
        "Register of Members and Directors",
        "Board Resolution",
        "Shareholder Resolution"
    ],
    "Licensing": [
        "Trade License Application",
        "Regulatory Approval Form",
        "Business Plan",
        "Passport Copy of Shareholders"
    ],
    "HR / Employment": [
        "Employment Contract",
        "Offer Letter",
        "Employee Handbook",
        "Non-Disclosure Agreement"
    ]
}

# Map keywords to standard document names
DOC_KEYWORD_MAP = {
    "articles": "Articles of Association",
    "aoa": "Articles of Association",
    "memorandum": "Memorandum of Association",
    "moa": "Memorandum of Association",
    "incorporation": "Incorporation Application Form",
    "application": "Incorporation Application Form",
    "ubo": "UBO Declaration Form",
    "ultimate beneficial": "UBO Declaration Form",
    "register of members": "Register of Members and Directors",
    "board resolution": "Board Resolution",
    "shareholder resolution": "Shareholder Resolution",
    "license": "Trade License Application",
    "licence": "Trade License Application",
    "employment contract": "Employment Contract",
    "offer letter": "Offer Letter",
    "handbook": "Employee Handbook",
    "nda": "Non-Disclosure Agreement",
    "kyc": "KYC Records",
}

# Example citations
CITATION_MAP = {
    "Articles of Association": "ADGM Companies Regulations 2020, Part 3, Section 12",
    "UBO Declaration Form": "Beneficial Ownership Regulations 2018, Section 5",
    "Employment Contract": "ADGM Employment Regulations (ER) 2019, Article X"
}


def get_legal_citation(doc_name: str) -> str:
    return CITATION_MAP.get(doc_name, "")


def normalize_uploaded_types(uploaded: List[str]) -> List[str]:
    normalized = []
    for u in uploaded:
        if not u:
            continue
        s = os.path.basename(u).lower()
        matched = None
        for kw, label in DOC_KEYWORD_MAP.items():
            if kw in s:
                matched = label
                break
        normalized.append(matched or os.path.splitext(os.path.basename(u))[0].title())

    # Deduplicate while keeping order
    seen = set()
    out = []
    for x in normalized:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def detect_process_from_uploaded(uploaded_normalized: List[str]) -> str:
    best = ("Unknown", 0)
    for process, checklist in CHECKLISTS.items():
        matches = sum(1 for doc in checklist if doc in uploaded_normalized)
        if matches > best[1]:
            best = (process, matches)
    return best[0]


def verify_document_checklist(uploaded_raw: List[str]) -> Dict:
    uploaded_normalized = normalize_uploaded_types(uploaded_raw)
    process = detect_process_from_uploaded(uploaded_normalized)
    result = {
        "process": process,
        "documents_uploaded": len(uploaded_normalized),
        "uploaded_documents": uploaded_normalized
    }
    if process in CHECKLISTS:
        required = CHECKLISTS[process]
        missing = [d for d in required if d not in uploaded_normalized]
        result["required_documents"] = len(required)
        if missing:
            result["missing_documents"] = [
                {"document": d, "legal_citation": get_legal_citation(d)}
                for d in missing
            ]
    else:
        result["required_documents"] = 0
        result["missing_documents"] = []
    return result
