def load_txt(file_path):
    text=open(file_path, "r", encoding="utf-8")
    return text.read() 