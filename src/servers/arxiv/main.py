from fastapi import FastAPI, Depends
from src.servers.arxiv.model import ArxivInput, ArxivOutput
from src.servers.arxiv.utils import arxiv_search
from langchain_community.utilities import ArxivAPIWrapper

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