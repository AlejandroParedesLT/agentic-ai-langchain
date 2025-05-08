
from langchain_community.tools.tavily_search import TavilySearchResults
from src.servers.websearch.model import WebSearchInput, WebSearchOutput
# import httpx


def simple_web_search(input:WebSearchInput, webSearchTool:TavilySearchResults) -> str:
    """
    Perform a simple web search using tavily.
    """
    try:
        results = webSearchTool.invoke(input.input)
        web_results = "\n".join([d["content"] for d in results])
        return WebSearchOutput(output=web_results)
    except Exception as e:
        return WebSearchOutput(output=str(e))