
from docx.shared import RGBColor, Pt
from docx.oxml import parse_xml

def insert_comment(paragraph, comment_text, color=(255,0,0), bold=True, italic=False, font_size=9):
    """
    python-docx does not support Word native comments reliably everywhere.
    Append a visible inline COMMENT tag for compatibility.
    """
    run = paragraph.add_run(f"  [COMMENT: {comment_text}]")
    try:
        run.font.color.rgb = RGBColor(*color)
    except Exception:
        pass
    run.font.bold = bold
    run.font.italic = italic
    run.font.size = Pt(font_size)

 
    try:
        highlight = parse_xml(r'<w:highlight xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:val="yellow"/>')
        run._element.rPr.append(highlight)
    except Exception:
        pass
