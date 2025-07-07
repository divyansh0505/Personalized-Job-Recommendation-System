import PyPDF2  #used for .pdf documents
import docx    #used python-docx for word documents

def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return " ".join([page.extract_text() for page in reader.pages])
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return " ".join([para.text for para in doc.paragraphs])
    else:
        return ""
