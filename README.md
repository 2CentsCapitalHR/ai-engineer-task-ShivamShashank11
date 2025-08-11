# ADGM-Compliant Corporate Agent with Document Intelligence

## Overview

AI-based legal assistant to review and validate business incorporation documents for Abu Dhabi Global Market (ADGM).  
Accepts `.docx` files, verifies required documents, flags issues, inserts comments, and generates reviewed files.

## Features

- Upload `.docx` legal documents
- Identify document types automatically
- Check completeness against ADGM checklist
- Detect red flags (missing clauses, incorrect jurisdiction, etc.)
- Insert inline comments referencing ADGM laws
- Output reviewed `.docx` with comments
- Generate JSON report summarizing findings

## Installation & Running

```bash
git clone https://github.com/2CentsCapitalHR/ai-engineer-task-ShivamShashank11.git
cd ai-engineer-task-ShivamShashank11
pip install -r requirements.txt
python app.py
```

Running on local URL: http://0.0.0.0:7860

- Running on public URL: https://018e4daaa06f0d1e80.gradio.live
  Open browser at http://localhost:7860 to use.

Usage
Upload one or more .docx files

Get reviewed documents with comments

Download JSON report with issues and missing docs

Example JSON output
json
Copy
Edit
{
"process": "Company Incorporation",
"documents_uploaded": 4,
"required_documents": 5,
"missing_document": "Register of Members and Directors",
"issues_found": [
{
"document": "Articles of Association",
"section": "Clause 3.1",
"issue": "Jurisdiction clause does not specify ADGM",
"severity": "High",
"suggestion": "Update jurisdiction to ADGM Courts."
}
]
}

## Screenshots

![Screenshot 1](./Screenshot%201.png)

![Screenshot 2](./Screenshot%202.png)
