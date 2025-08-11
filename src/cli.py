# src/cli.py
import argparse
import os
from .checklist_verifier import verify_document_checklist
from .document_processor import process_document  # Corrected import
from .file_utils import write_json


def main():
    parser = argparse.ArgumentParser(description="ADGM Compliance Document Checker")
    parser.add_argument("--input", required=True, help="Path to input .docx file")
    parser.add_argument("--output", required=True, help="Directory to save reviewed file and report")
    args = parser.parse_args()

    # Ensure output directory exists
    os.makedirs(args.output, exist_ok=True)

    # 1️⃣ Verify checklist
    print("[1/3] Verifying checklist...")
    checklist_result = verify_document_checklist(args.input)
    print(f"Detected process: {checklist_result.get('process', 'Unknown')}")
    print(f"Missing documents: {checklist_result.get('missing_documents', [])}")

    # 2️⃣ Process document
    print("[2/3] Processing document...")
    result = process_document(
        args.input,
        checklist_result=checklist_result,
        output_dir=args.output,
        debug=False
    )

    # 3️⃣ Save report
    print("[3/3] Generating report...")
    report_path = os.path.join(args.output, "review_report.json")
    write_json(result, report_path)

    # ✅ Done
    print("\n✅ Review complete.")
    print(f"Reviewed document: {result.get('reviewed_path', 'None')}")
    print(f"Report saved: {report_path}")


if __name__ == "__main__":
    main()
