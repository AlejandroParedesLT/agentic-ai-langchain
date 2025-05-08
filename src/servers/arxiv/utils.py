from langchain_community.utilities import ArxivAPIWrapper
from src.servers.arxiv.model import ArxivOutput, ArxivInput

def arxiv_search(input: ArxivInput, executor: ArxivAPIWrapper) -> ArxivOutput:
    """
    Perform a simple search using arxiv
    """
    try:
        results = executor.run(input.input)
        return ArxivOutput(output=results)
    except Exception as e:
        return ArxivOutput(output=str(e))