from src.servers.hallucinationGrader.model import hallucinationGraderInput, hallucinationGraderOutput
from src.servers.hallucinationGrader.utils import gradeAnswer
from fastapi import FastAPI, Depends
from src.models.ollama import llmservice
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

llm_json_mode = llmservice(model_id=os.getenv('LLM_ID'), temperature=os.getenv('LLM_TEMPERATURE'), format=os.getenv('LLM_format'))

def instanceLLM()->llmservice:
    return llm_json_mode

@app.post("/process", response_model=hallucinationGraderOutput)
async def process_gradeAnswer(
    input: hallucinationGraderInput,
    llm:llmservice = Depends(instanceLLM)) -> hallucinationGraderOutput:
    """Process a web search request."""
    return gradeAnswer(input, llm)
