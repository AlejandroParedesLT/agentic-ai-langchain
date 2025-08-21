# from src.servers.websearch.utils import simple_web_search
# from src.servers.websearch.model import WebSearchInput, WebSearchOutput

from utils import simple_web_search
from model import WebSearchInput, WebSearchOutput

from fastapi import FastAPI, Depends
from langchain_community.tools.tavily_search import TavilySearchResults

##############################
# Pending implementation for DuckDuckGoSearchRun``
# from langchain_community.tools import DuckDuckGoSearchRun
# search = DuckDuckGoSearchRun()
# search.invoke("Obama's first name?")

app = FastAPI()
web_search_tool = TavilySearchResults(k=3)

def instanceWebSearch()->TavilySearchResults:
    return web_search_tool

@app.post("/process", response_model=WebSearchOutput)
async def process_websearch(
    prompt: WebSearchInput,
    webSearchTools: TavilySearchResults = Depends(instanceWebSearch) 
    ) -> WebSearchOutput:
    """Process a web search request."""
    return simple_web_search(prompt, webSearchTools)
