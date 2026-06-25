import os
from typing import(List)
from app.rag.chunking import chunk_text
from app.rag.embedding import get_embedding
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
CHROMA_DIR = "./chroma_db"
def store_document(text:str)->int:
    chunks=chunk_text(text)
    db = Chroma(persist_directory=CHROMA_DIR, embedding_function=get_embedding())
    db.add_texts(texts=chunks)
    db.persist()
    return len(chunks)

def search_document(query:str, k:int=3)->List[Document]:
    SIMILARITY_THRESHOLD=0.7
    if not os.path.exists(CHROMA_DIR):
        return "Please upload documents first."
    db = Chroma(persist_directory=CHROMA_DIR, embedding_function=get_embedding())
    docs = db.similarity_search_with_score(query, k=k)
    return docs