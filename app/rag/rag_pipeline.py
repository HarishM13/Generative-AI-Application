import json
from app.db.db_retriever import search_document
from app.rag.llm import get_llm
from app.rag.prompt import build_prompt

def generate_answer(question:str)->json:
    docs=search_document(question)
    context="\n---\n".join([doc.page_content for doc in docs])
    llm=get_llm()
    result=llm.invoke(build_prompt(context,question))
    return {"answer":result.content,"sources":[doc.page_content for doc in docs]}
