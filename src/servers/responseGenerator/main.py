from typing import Any
from src.servers.responseGenerator.model import GeneratorResponseInput, GeneratorResponseOutput
from src.servers.responseGenerator.utils import generate
from fastapi import FastAPI, Depends
from src.models.ollama import llmservice
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

llm = llmservice(model_id=os.getenv('LLM_ID'), temperature=os.getenv('LLM_TEMPERATURE'))

def instanceLLM()->llmservice:
    return llm 

@app.post("/process", response_model=GeneratorResponseOutput)
async def generator(
    input: GeneratorResponseInput,
    llm:llmservice = Depends(instanceLLM)
    ) -> GeneratorResponseOutput:
    """Process a web search request."""
    return generate(input, llm)
