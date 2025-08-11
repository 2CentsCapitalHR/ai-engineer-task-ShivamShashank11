
import gradio as gr
import os
import io
import zipfile
from datetime import datetime
from src.document_processor import process_document
from src.checklist_verifier import verify_document_checklist
from src.report_generator import generate_report

LEGAL_REFERENCES = {
    "Memorandum of Association": "ADGM Companies Regulations 2020, Section 12(1)",
    "Incorporation Application Form": "ADGM Companies Regulations 2020, Section 7",
    "UBO Declaration Form": "Beneficial Ownership Regulations 2018, Section 5",
    "Register of Members and Directors": "ADGM Companies Regulations 2020, Schedule 1, Part 3",
    "Board Resolution": "ADGM Companies Regulations 2020, Section 73",
    "Shareholder Resolution": "ADGM Companies Regulations 2020, Section 74",
}


required_docs = [
    "Memorandum of Association",
    "Incorporation Application Form",
    "UBO Declaration Form",
    "Register of Members and Directors",
    "Board Resolution",
    "Shareholder Resolution"
]

def analyze_documents(filepaths, debug=False):
    """
    filepaths: list of filepaths (strings) from gradio Files
    returns: (report dict, zip path or None)
    """
    if not filepaths:
        return {"error": "No files uploaded."}, None

  
    checklist_result = verify_document_checklist(list(filepaths))


    processed_docs = []
    reviewed_paths = []
    for fp in filepaths:
        if debug:
            print("[DEBUG] Processing:", fp)
        result = process_document(fp, checklist_result=checklist_result, debug=debug)
        processed_docs.append(result)
        if result.get("reviewed_path"):
            reviewed_paths.append(result["reviewed_path"])


    detected_process = checklist_result.get("process", "Unknown")
    final_report = generate_report(processed_docs, checklist_result, detected_process)

    zip_path = None
    if reviewed_paths:
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
            for p in reviewed_paths:
                if p and os.path.exists(p):
                    z.write(p, arcname=os.path.basename(p))
        buf.seek(0)
        os.makedirs("tmp_reviewed", exist_ok=True)
        zip_filename = f"reviewed_docs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        zip_path = os.path.join("tmp_reviewed", zip_filename)
        with open(zip_path, "wb") as fh:
            fh.write(buf.read())

    return final_report, zip_path


with gr.Blocks() as demo:
    gr.Markdown("# 📄 ADGM Corporate Agent — MVP")
    gr.Markdown("Upload one or more `.docx` files for ADGM compliance review.")

    with gr.Row():
        file_input = gr.Files(label="Upload .docx files", file_types=[".docx"], type="filepath")
        debug_check = gr.Checkbox(label="Enable debug logs in console", value=False)

    analyze_button = gr.Button("🔍 Analyze Documents", variant="primary")

    with gr.Row():
        output_json = gr.JSON(label="📊 Analysis Report (JSON)")
        output_zip = gr.File(label="⬇ Download Reviewed Documents (.zip)")

    analyze_button.click(
        fn=analyze_documents,
        inputs=[file_input, debug_check],
        outputs=[output_json, output_zip]
    )

if __name__ == "__main__":
    demo.launch(share=True, server_name="0.0.0.0", server_port=7860)
