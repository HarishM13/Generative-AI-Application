from langchain_text_splitters import RecursiveCharacterTextSplitter
def chunk_text(raw_text:str)->list[str]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120
    )
    chunks = text_splitter.split_text(raw_text)
    return chunks