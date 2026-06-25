import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
def get_llm():
    return ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview", temperature=0.5,google_api_key=os.environ.get("GOOGLE_API_KEY"))
