import os
import json
import zipfile
from docx import Document
from tempfile import TemporaryDirectory

def analyze_documents(files):
    required_docs = [
        ("Incorporation Application Form", ""),
        ("Articles of Association", "ADGM Companies Regulations 2020, Part 3, Section 12"),
        ("Memorandum of Association", ""),
        ("UBO Declaration Form", "Beneficial Ownership Regulations 2018, Section 5"),
        ("Register of Members and Directors", ""),
        ("Board Resolution", ""),
        ("Shareholder Resolution", "")
    ]

    uploaded_names = []
    reviewed_files = []
    issues = []

    with TemporaryDirectory() as tmpdir:
        for f in files:
            doc = Document(f.name)
            fname = os.path.basename(f.name)
            uploaded_names.append(fname)

       
            text = "\n".join([p.text for p in doc.paragraphs])
            if not any(str(i) + "." in text for i in range(1, 5)):
                issues.append({
                    "document": fname,
                    "issue": "Document appears to lack numbered clauses/section headings.",
                    "severity": "Low",
                    "suggestion": "Use numbered clause headings (1., 1.1, 2., etc.) to improve clarity.",
                    "paragraph_index": None,
                    "legal_reference": "ADGM Best Practice Templates — Use numbered clauses for clarity."
                })

           
            reviewed_path = os.path.join(tmpdir, fname.replace(".docx", "_reviewed.docx"))
            doc.save(reviewed_path)
            reviewed_files.append(reviewed_path)

       
        missing_docs = [
            {"document": req[0], "legal_citation": req[1]}
            for req in required_docs if req[0] not in uploaded_names
        ]

      
        zip_path = os.path.join(tmpdir, "reviewed_docs.zip")
        with zipfile.ZipFile(zip_path, "w") as zf:
            for rf in reviewed_files:
                zf.write(rf, os.path.basename(rf))

       
        report = {
            "process": "Company Incorporation",
            "documents_uploaded": len(uploaded_names),
            "required_documents": len(required_docs),
            "uploaded_documents": uploaded_names,
            "missing_documents": missing_docs,
            "issues_found": issues,
            "reviewed_files": reviewed_files,
            "total_issues": len(issues),
            "high_severity_count": sum(1 for i in issues if i["severity"] == "High"),
            "severity_buckets": {
                "high": sum(1 for i in issues if i["severity"] == "High"),
                "medium": sum(1 for i in issues if i["severity"] == "Medium"),
                "low": sum(1 for i in issues if i["severity"] == "Low"),
            }
        }

        return report, zip_path
