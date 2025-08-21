from langchain_community.utilities import ArxivAPIWrapper
# from src.servers.arxiv.model import ArxivOutput, ArxivInput
from model import ArxivOutput, ArxivInput

def arxiv_search(input: ArxivInput, executor: ArxivAPIWrapper) -> ArxivOutput:
    """
    Perform a simple search using arxiv
    Args:
        input (str): Input containing an explicit search query or DOI (better to use DOI if available).
    returns:
        output (str): The result of the search.
    """
    try:
        results = executor.run(input.input)
        return ArxivOutput(output=results)
    except Exception as e:
        return ArxivOutput(output=str(e))