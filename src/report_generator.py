
def _severity_buckets(issues):
    buckets = {"high": [], "medium": [], "low": []}
    for it in issues:
        sev = (it.get("severity") or "").lower()
        if sev.startswith("h"):
            buckets["high"].append(it)
        elif sev.startswith("m"):
            buckets["medium"].append(it)
        else:
            buckets["low"].append(it)
    return buckets

def generate_report(processed_docs, checklist_result, detected_process):
    issues_combined = []
    reviewed_files = []
    for pd in processed_docs:
        fname = pd.get("file_name", "Unknown")
        for it in pd.get("issues", []):
            issues_combined.append({
                "document": fname,
                "issue": it.get("issue",""),
                "severity": it.get("severity",""),
                "suggestion": it.get("suggestion",""),
                "paragraph_index": it.get("paragraph_index"),
                "legal_reference": it.get("legal_reference","")
            })
        if pd.get("reviewed_path"):
            reviewed_files.append(pd["reviewed_path"])

    buckets = _severity_buckets(issues_combined)

    report = {
        "process": detected_process or checklist_result.get("process","Unknown"),
        "documents_uploaded": checklist_result.get("documents_uploaded", len(processed_docs)),
        "required_documents": checklist_result.get("required_documents", 0),
        "uploaded_documents": checklist_result.get("uploaded_documents", []),
        "missing_documents": checklist_result.get("missing_documents", []),
        "issues_found": issues_combined,
        "reviewed_files": reviewed_files,
        "total_issues": len(issues_combined),
        "high_severity_count": len(buckets["high"]),
        "severity_buckets": {"high": len(buckets["high"]), "medium": len(buckets["medium"]), "low": len(buckets["low"])}
    }
    return report
