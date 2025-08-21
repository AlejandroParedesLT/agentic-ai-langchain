# from src.servers.documentGrader.utils import grade_documents
# from src.servers.documentGrader.model import GraderInput, GraderOutput
# from src.models.ollama import llmservice

from utils import grade_documents
from model import GraderInput, GraderOutput
from langchain_ollama import ChatOllama
from fastapi import FastAPI, Depends
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# llm_json_mode = llmservice(model_id=os.getenv('LLM_ID'), temperature=os.getenv('LLM_TEMPERATURE'), format=os.getenv('LLM_format'))
llm_json_mode=ChatOllama(model=os.getenv('LLM_ID'), temperature=os.getenv('LLM_TEMPERATURE'),format=os.getenv('LLM_format'), base_url="http://host.docker.internal:11434")

def return_llm_json_mode()-> ChatOllama:
    return llm_json_mode

@app.post("/process", response_model=GraderOutput)
async def process_document_grade(
    prompt: GraderInput,
    llm:ChatOllama = Depends(return_llm_json_mode)
    ) -> GraderOutput:
    """Process a web search request."""
    return grade_documents(prompt, llm)
