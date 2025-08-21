# from src.servers.hallucinationGrader.model import hallucinationGraderInput, hallucinationGraderOutput
# from src.servers.hallucinationGrader.utils import gradeAnswer
# from src.models.ollama import llmservice

from model import hallucinationGraderInput, hallucinationGraderOutput
from utils import gradeAnswer
from langchain_ollama import ChatOllama


from fastapi import FastAPI, Depends
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

llm_json_mode=ChatOllama(model=os.getenv('LLM_ID'), temperature=os.getenv('LLM_TEMPERATURE'),format=os.getenv('LLM_format'), base_url="http://host.docker.internal:11434")

def instanceLLM()->ChatOllama:
    return llm_json_mode

@app.post("/process", response_model=hallucinationGraderOutput)
async def process_gradeAnswer(
    input: hallucinationGraderInput,
    llm:ChatOllama = Depends(instanceLLM)) -> hallucinationGraderOutput:
    """Process a web search request."""
    return gradeAnswer(input, llm)
