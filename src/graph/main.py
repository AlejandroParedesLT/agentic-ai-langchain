from fastapi import FastAPI, Depends
from src.graph.flow_graph import ServerState, LangchainGraph
import os
from dotenv import load_dotenv
load_dotenv()
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Fast API internall
app = FastAPI()

graph = LangchainGraph() 
graph = graph.compile_graph()

def instanceGraph()->LangchainGraph:
    return graph

@app.post("/generate", response_model=ServerState)
async def generate(
    prompt: ServerState,
    LangchainGraph: LangchainGraph = Depends(instanceGraph)
    ) -> ServerState:
    """Process a web search request."""
    result = await LangchainGraph.invoke(prompt)
    return result
