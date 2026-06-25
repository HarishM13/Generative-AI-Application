import os
import logging
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, UploadFile, File
from app.ingestion.document_manager import process_document
from app.db.db_retriever import store_document
from app.agents.agent_manager import execute_agent_manager
router = APIRouter()

class QueryRequest(BaseModel):
    user_query: str

logger = logging.getLogger(__name__)
greetings={"hello", "hi", "hey", "greetings", "good morning", "good afternoon", "hola", "how are you"}

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    try:
        with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())
        
        processDoc= process_document(temp_path)
        chunks=store_document(text=processDoc)
        return {"message": f"Successfully ingested and indexed {file.filename}","chunks":chunks}
    except Exception as e:
        print(f"Exception is {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.get("/query")
def execute_agentic_pipeline(request: QueryRequest):
    user_query=request.user_query
    try:
        clean_query = user_query.lower().strip()
        if clean_query in greetings or any(clean_query.startswith(g) for g in greetings if len(g) > 2):
            return {
                "status": "Greeting",
                "user_query": user_query,
                "final_verified_response": "Hello! I am your AI assistant.How can I help you "
            } 
        else:
            result = execute_agent_manager(user_query)
            return result
    except Exception as ex:
         logger.exception(f"Retriever error: {str(ex)}")