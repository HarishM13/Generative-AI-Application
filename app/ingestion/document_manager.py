import os
import re
from app.ingestion.pdf_upload import load_pdf
from app.ingestion.text_upload import load_txt
from app.ingestion.csv_upload import load_csv
from app.ingestion.excel_upload import load_excel
from app.utils.util import clean_text






def process_document(path: str)->str:
    ext = os.path.splitext(path)[1].lower()
    if ext==".pdf":return clean_text(load_pdf(path))
    elif ext==".txt":return clean_text(load_txt(path))
    elif ext==".csv":return clean_text(load_csv(path))
    elif ext==".xlsx":return clean_text(load_excel(path))
    else:
        raise ValueError(f"Unsupported file format: {ext}")
    