from pypdf import PdfReader
def load_pdf(file_path:str)->str:
    text=""
    reader = PdfReader(file_path)
    for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    return text