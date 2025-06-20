from pdfminer.high_level import extract_text
import docx

def extract_text_from_pdf(path):
    return extract_text(path)

def extract_text_from_docx(path):
    doc = docx.Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text_from_file(path, filename):
    if filename.lower().endswith('.pdf'):
        return extract_text_from_pdf(path)
    elif filename.lower().endswith(('.doc', '.docx')):
        return extract_text_from_docx(path)
    else:
        return ''
