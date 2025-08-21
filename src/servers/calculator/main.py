
# from src.servers.calculator.utils import calculator
# from src.servers.calculator.model import CalculatorInput, CalculatorOutput
from utils import calculator
from model import CalculatorInput, CalculatorOutput
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI()

@app.post("/process", response_model=CalculatorOutput)
async def process_websearch(prompt: CalculatorInput) -> CalculatorOutput:
    """Process a web search request."""
    return calculator(prompt)

@app.get("/docstring")
async def getdocstring() -> str:
    return calculator.__doc__

# Add the MCP server to your FastAPI app
mcp = FastApiMCP(
    app,  
    name="Calculator with parser from string",  # Name for your MCP server
    description=calculator.__doc__,
    describe_all_responses=True,  # Include all possible response schemas
    describe_full_response_schema=True  # Include full JSON schema in descriptions
)

# Mount the MCP server to your FastAPI app
mcp.mount()

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)