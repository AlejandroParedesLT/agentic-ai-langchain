from fastapi import FastAPI, Depends
# from src.servers.arxiv.model import ArxivInput, ArxivOutput
# from src.servers.arxiv.utils import arxiv_search
from model import ArxivInput, ArxivOutput
from utils import arxiv_search


from langchain_community.utilities import ArxivAPIWrapper
from fastapi_mcp import FastApiMCP

app = FastAPI()
arxiv_executor = ArxivAPIWrapper()  # instantiate once


def get_arxiv_executor() -> ArxivAPIWrapper:
    return arxiv_executor


@app.post("/process", response_model=ArxivOutput)
async def process_vectordbsearch(
    input: ArxivInput,
    executor: ArxivAPIWrapper = Depends(get_arxiv_executor),
) -> ArxivOutput:
    return arxiv_search(input, executor)

@app.get("/docstring")
async def getdocstring() -> str:
    return arxiv_search.__doc__


# Add the MCP server to your FastAPI app
mcp = FastApiMCP(
    app,  
    name="Arxiv Search",  # Name for your MCP server
    description=arxiv_search.__doc__,
    describe_all_responses=True,  # Include all possible response schemas
    describe_full_response_schema=True  # Include full JSON schema in descriptions
)

# Mount the MCP server to your FastAPI app
mcp.mount()

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)