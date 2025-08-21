import operator
from typing_extensions import TypedDict
from typing import List, Annotated
from langgraph.graph import StateGraph
from IPython.display import Image, display
from typing import Any, TypedDict

# from src.models.ollama import llmservice
import httpx
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph
from langgraph.graph import END
from dotenv import load_dotenv
import os
load_dotenv()

class CustomStateModel(TypedDict):
    question: str  # User question
    generation: str  # LLM generation
    max_retries: int  # Max number of retries for answer generation
    loop_step: Annotated[int, operator.add] # 
    conversation: List[dict] # Conversation history
    tools_results: str # Web search result

class ServerState(TypedDict):
    payload: Any

def call_mcp_server(url):
    async def fn(state: ServerState) -> ServerState:
        print(f"[DEBUG] Calling {url} with payload:", state["payload"])
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=state["payload"])
            response.raise_for_status()
            return {"payload": response.json()}
    return RunnableLambda(fn).with_config({"run_name": f"CallMCP::{url.split(':')[2]}"})


SERVICE_ALIASES ={
    "arxiv": os.getenv('arxiv', "http://arxiv:8000/process"),
    "calculator": os.getenv('calculator', "http://calculator:8000/process"),
    "coding": os.getenv('coding', "http://coding:8000/process"),
    "dataAnalysis": os.getenv('dataAnalysis', "http://dataAnalysis:8000/process"),
    "websearch":os.getenv('websearch', "http://websearch:8000/process"),
    "vectordb":os.getenv('vectordb', "http://vectordb:8000/process"),

    "documentGrader": os.getenv('documentGrader', "http://documentGrader:8000/process"),
    "routers":os.getenv('routers', "http://routers:8000/process"),
    "hallucinationGrader":os.getenv('hallucinationGrader', "http://hallucinationGrader:8000/process"),
    "responseGenerator":os.getenv('responseGenerator', "http://responseGenerator:8000/process"),
}

def decide_to_generate(state):
    """
    Determines whether to generate an answer, or add web search

    Args:
        state (dict): The current graph state

    Returns:
        str: Binary decision for next node to call
    """

    print("---ASSESS GRADED DOCUMENTS---")
    web_search = state["web_search"]
    if web_search == "Yes":
        # All documents have been filtered check_relevance
        # We will re-generate a new query
        print(
            "---DECISION: NOT ALL DOCUMENTS ARE RELEVANT TO QUESTION, INCLUDE WEB SEARCH---"
        )
        return "websearch"
    else:
        # We have relevant documents, so generate answer
        print("---DECISION: GENERATE---")
        return "generate"


class LangchainGraph:
    def __init__(self):
        self.workflow = StateGraph(ServerState)
        self.graph = None

    def compile_graph(self):
        """
        Compile the graph and add edges between nodes
        """
        # Define the nodes
        self.workflow.add_node("websearch", call_mcp_server(SERVICE_ALIASES['websearch']))
        self.workflow.add_node("arxiv", call_mcp_server(SERVICE_ALIASES['arxiv']))
        self.workflow.add_node("calculator", call_mcp_server(SERVICE_ALIASES['calculator']))  
        self.workflow.add_node("coding", call_mcp_server(SERVICE_ALIASES['coding'])) 
        self.workflow.add_node("dataAnalysis", call_mcp_server(SERVICE_ALIASES['dataAnalysis']))
        self.workflow.add_node("vectordb", call_mcp_server(SERVICE_ALIASES['vectordb'])) 
        
        self.workflow.add_node("grade_documents", call_mcp_server(SERVICE_ALIASES['documentGrader']))
        self.workflow.add_node("responseGenerator", call_mcp_server(SERVICE_ALIASES['responseGenerator']))

        # Build graph
        self.workflow.set_conditional_entry_point(
            call_mcp_server(SERVICE_ALIASES['routers']),
            {
                "websearch": "websearch",
                "vectordb": "vectordb",
                "coding": "coding",
                "arxiv": "arxiv",
                "dataAnalysis": "dataAnalysis",
            },
        )
        self.workflow.add_edge("websearch", "responseGenerator")
        self.workflow.add_edge("coding", "responseGenerator")
        self.workflow.add_edge("arxiv", "responseGenerator")
        self.workflow.add_edge("dataAnalysis", "responseGenerator")
        self.workflow.add_edge("vectordb", "grade_documents")
        self.workflow.add_conditional_edges(
            "grade_documents",
            decide_to_generate,
            {
                "websearch": "websearch",
                "generate": "responseGenerator",
            },
        )
        self.workflow.add_conditional_edges(
            "responseGenerator",
            call_mcp_server(SERVICE_ALIASES['hallucinationGrader']),
            {
                "not supported": "responseGenerator",
                "useful": END,
                "not useful": "websearch",
                "max retries": END,
            },
        )
        self.graph = self.workflow.compile()
        return self.graph


    def display_graph(self):
        """
        Display the graph using IPython display
        """
        # self.graph.render("graph", format="png")
        display(Image(self.graph.get_graph().draw_mermaid_png()))