# from src.servers.responseGenerator.model import GeneratorResponseInput, GeneratorResponseOutput
# from src.servers.responseGenerator.utils import generate
# from src.models.ollama import llmservice

from model import GeneratorResponseInput, GeneratorResponseOutput
from utils import generate
from langchain_ollama import ChatOllama

from fastapi import FastAPI, Depends
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

llm=ChatOllama(model=os.getenv('LLM_ID'), temperature=os.getenv('LLM_TEMPERATURE'), base_url="http://host.docker.internal:11434")


def instanceLLM()->ChatOllama:
    return llm 

@app.post("/process", response_model=GeneratorResponseOutput)
async def generator(
    input: GeneratorResponseInput,
    llm:ChatOllama = Depends(instanceLLM)
    ) -> GeneratorResponseOutput:
    """Process a web search request."""
    return generate(input, llm)
