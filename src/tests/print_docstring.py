
from langchain_community.tools.tavily_search import TavilySearchResults
from src.servers.websearch.model import WebSearchInput, WebSearchOutput
# import httpx
from smolagents import CodeAgent, DuckDuckGoSearchTool, InferenceClientModel, VisitWebpageTool, FinalAnswerTool, Tool, tool
import inspect
from typing import get_type_hints


# print("Test Hello World")
@tool
def simple_web_search(input:WebSearchInput, webSearchTool:TavilySearchResults) -> str:
    """
    Perform a simple web search using Tavily.

    Args:
        input (WebSearchInput): The input parameters for the web search.
        webSearchTool (TavilySearchResults): The Tavily search tool instance.

    Returns:
        str: The search results as a string.
    """
    try:
        results = webSearchTool.invoke(input.input)
        web_results = "\n".join([d["content"] for d in results])
        return WebSearchOutput(output=web_results)
    except Exception as e:
        return WebSearchOutput(output=str(e))

if __name__ == "__main__":
    # Accessing metadata
    print(f"Tool Name: {simple_web_search.name}")
    print(f"Description: {simple_web_search.description}")
    print(f"Inputs: {simple_web_search.inputs}")
    print(f"Output Type: {simple_web_search.output_type}")