# from src.servers.vectordb.utils import vectordb_search
# from src.servers.vectordb.model import VectorSearch,VectorSearchInput,VectorSearchOutput

from utils import vectordb_search
from model import VectorSearch,VectorSearchInput,VectorSearchOutput

from fastapi import FastAPI, Depends

app = FastAPI()

# Instance Vector DB
urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]
vectorDB = VectorSearch(cnx='Webbase')
vectorDB.load_urls(urls)

def vectorDBinstance() -> VectorSearch:
    return vectorDB 


@app.post("/process", response_model=VectorSearchOutput)
async def process_vectordbsearch(
    input: VectorSearchInput,
    vectorDB: VectorSearch = Depends(vectorDBinstance)
    ) -> VectorSearchOutput:
    """Process a web search request."""
    return vectordb_search(input, vectorDB)
