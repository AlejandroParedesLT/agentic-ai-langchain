
from src.servers.vectordb.model import VectorSearchInput,VectorSearchOutput,VectorSearch

def vectordb_search(input: VectorSearchInput, vectorDB:VectorSearch) -> VectorSearchOutput:
    """
    Perform a simple web search using tavily.
    """
    try:
        results = vectorDB.retriever.invoke(input.input)
        web_results = "\n".join([d["content"] for d in results])
        return VectorSearchOutput(output=web_results)
    except Exception as e:
        return VectorSearchOutput(output=str(e))