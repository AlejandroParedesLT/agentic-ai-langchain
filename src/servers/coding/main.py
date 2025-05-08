from src.servers.coding.utils import execute_code
from src.servers.coding.model import CodingInput, CodingOutput
from fastapi import FastAPI

app = FastAPI()

@app.post("/process", response_model=CodingOutput)
async def process_codeExecution(prompt: CodingInput) -> CodingOutput:
    """Process a web search request."""
    return execute_code(prompt)
