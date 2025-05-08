from typing import Any
from src.servers.routers.model import RouterInput, RouterOutput
from src.servers.routers.utils import route_question
from fastapi import FastAPI, Depends
from src.models.ollama import llmservice
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

llm_json_mode = llmservice(model_id=os.getenv('LLM_ID'), temperature=os.getenv('LLM_TEMPERATURE'), format=os.getenv('LLM_format'))

def llmInstance()->llmservice:
    return llm_json_mode

@app.post("/process", response_model=RouterOutput)
async def process_route(
    input: RouterInput,
    llm:llmservice = Depends(llmInstance)
    ) -> RouterOutput:
    """Process a web search request."""
    return route_question(input, llm)
