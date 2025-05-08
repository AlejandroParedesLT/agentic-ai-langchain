
from src.servers.calculator.utils import calculator
from src.servers.calculator.model import CalculatorInput, CalculatorOutput
from fastapi import FastAPI


app = FastAPI()

@app.post("/process", response_model=CalculatorOutput)
async def process_websearch(prompt: CalculatorInput) -> CalculatorOutput:
    """Process a web search request."""
    return calculator(prompt)