# from src.servers.router.model import RouterInput, RouterOutput
# from src.servers.router.utils import route_question
# from src.models.ollama import llmservice

from model import RouterInput, RouterOutput
from utils import route_question
from langchain_ollama import ChatOllama


from fastapi import FastAPI, Depends
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

llm_json_mode=ChatOllama(model=os.getenv('LLM_ID'), temperature=os.getenv('LLM_TEMPERATURE'),format=os.getenv('LLM_format'), base_url="http://host.docker.internal:11434")

def llmInstance()->ChatOllama:
    print("llmInstance, connected")
    print(os.getenv('LLM_ID'))
    return llm_json_mode

@app.post("/process", response_model=RouterOutput)
async def process_route(
    input: RouterInput,
    llm:ChatOllama = Depends(llmInstance)
    ) -> RouterOutput:
    """Process a web search request."""
    return route_question(input, llm)
