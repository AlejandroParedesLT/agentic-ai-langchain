### Search
from langchain_community.tools.tavily_search import TavilySearchResults

class TavilySearchResults(TavilySearchResults):
    """Tool that queries the Tavily Search API and gets back json."""

    def __init__(self, k=5, **kwargs):
        super().__init__(**kwargs)
        self.k = k

    def _run(self, query: str) -> str:
        results = super()._run(query)
        return results[:self.k]