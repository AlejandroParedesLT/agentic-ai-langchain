
# from src.servers.vectordb.model import VectorSearchInput,VectorSearchOutput,VectorSearch
from model import VectorSearchInput,VectorSearchOutput,VectorSearch

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs if doc.page_content)

def vectordb_search(input: VectorSearchInput, vectorDB:VectorSearch) -> VectorSearchOutput:
    """
    Perform a simple web search using tavily.
    """
    try:
        docs = vectorDB.retriever.invoke(input.input)
        docs_txt = format_docs(docs)
        return VectorSearchOutput(output=docs_txt)
    except Exception as e:
        return VectorSearchOutput(output=str(e))