<<<<<<< HEAD
[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/vgbm4cZ0)
=======
# ADGM-Compliant Corporate Agent with Document Intelligence

## Overview

This project is an AI-powered legal assistant designed to assist users in reviewing, validating, and preparing legal documentation for business incorporation and compliance within the Abu Dhabi Global Market (ADGM) jurisdiction.  
The Corporate Agent accepts `.docx` documents, verifies completeness based on ADGM rules, highlights red flags, inserts contextual comments, and generates reviewed downloadable files. It also notifies users of missing mandatory documents based on a predefined checklist.

## Features

- Accepts `.docx` legal documents upload
- Automatically identifies document types
- Verifies completeness against ADGM required document checklists
- Detects legal red flags such as ambiguous language, incorrect jurisdiction, and missing clauses
- Inserts inline comments with relevant ADGM legal references
- Outputs reviewed `.docx` files with annotations
- Generates structured JSON reports summarizing the analysis
- Uses Retrieval-Augmented Generation (RAG) for legal accuracy

## Supported Document Types

- Articles of Association (AoA)
- Memorandum of Association (MoA)
- Board Resolution Templates
- Shareholder Resolution Templates
- Incorporation Application Form
- UBO Declaration Form
- Register of Members and Directors
- Change of Registered Address Notice
- Licensing Regulatory Filings
- Employment HR Contracts
- Commercial Agreements
- Compliance Risk Policies

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Install dependencies with pip

### Installation

```bash
git clone https://github.com/2CentsCapitalHR/ai-engineer-task-ShivamShashank11.git
cd ai-engineer-task-ShivamShashank11
pip install -r requirements.txt
Running the Application

python app.py
Then open your browser and navigate to http://localhost:7860 to upload .docx files and start analyzing documents.

Usage
Upload one or more .docx legal documents.

The system will analyze document completeness and compliance with ADGM rules.

Download the reviewed documents with inline comments.

View JSON reports summarizing detected issues and any missing documents.

Example JSON Output

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
Screenshots




![Screenshot 1](./Screenshot%201.png)



![Screenshot 2](./Screenshot%202.png)

```
>>>>>>> c547088 (Initial commit: Add project files excluding venv)
