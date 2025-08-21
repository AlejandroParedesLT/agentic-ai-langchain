import operator
from typing_extensions import TypedDict
from typing import List, Annotated
from langgraph.graph import StateGraph
from IPython.display import Image, display
from typing import Any, TypedDict

from langchain_ollama import ChatOllama
# from src.graph.utils.langLambdas import decide_to_generate
from utils.langLambdas import decide_to_generate

import httpx
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph
from langgraph.graph import END
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages


import os
load_dotenv()

MCP_TOOLS_SERVICE_ALIASES ={
    "arxiv": os.getenv('arxiv', "http://arxiv:8000/process"),
    "calculator": os.getenv('calculator', "http://calculator:8000/process"),
    "coding": os.getenv('coding', "http://coding:8000/process"),
    "dataAnalysis": os.getenv('dataAnalysis', "http://dataAnalysis:8000/process"),
    "websearch":os.getenv('websearch', "http://websearch:8000/process"),
    "vectordb":os.getenv('vectordb', "http://vectordb:8000/process"),

    "documentGrader": os.getenv('documentGrader', "http://documentGrader:8000/process"),
    "router":os.getenv('router', "http://router:8000/process"),
    "hallucinationGrader":os.getenv('hallucinationGrader', "http://hallucinationGrader:8000/process"),
    "responseGenerator":os.getenv('responseGenerator', "http://responseGenerator:8000/process"),
}

def llmInstance()->ChatOllama:
    print("llmInstance, connected")
    print(os.getenv('LLM_ID'))
    llm_json_mode = ChatOllama(model=os.getenv("LLM_MODEL"), temperature=os.getenv('LLM_TEMPERATURE'), format=os.getenv('LLM_format'))
    return llm_json_mode

def getTools()->List[RunnableLambda]:
    """
    Get the tools to be used in the graph.
    """
    tools = []
    for tool in MCP_TOOLS_SERVICE_ALIASES:
        tools.append(
            RunnableLambda(
                lambda x, tool=tool: httpx.post(MCP_TOOLS_SERVICE_ALIASES[tool], json=x).json()
            )
        )
    return tools

class CustomStateModel(TypedDict):
    """
    LangGraph state model for the application
    """
    messages: Annotated[list, add_messages]
    max_retries: int  # Max number of retries for answer generation
    loop_step: Annotated[int, operator.add] # 
    conversation: List[dict] # Conversation history
    tools_results: str # Web search result

class ServerState(TypedDict):
    """
    Intermediate state for the server.
    """
    payload: Any

def call_mcp_server(url):
    async def fn(state: ServerState) -> ServerState:
        print(f"[DEBUG] Calling {url} with payload:", state["payload"])
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=state["payload"])
            response.raise_for_status()
            return {"payload": response.json()}
    return RunnableLambda(fn).with_config({"run_name": f"CallMCP::{url.split(':')[2]}"})


class CustomLangGraph:
    def __init__(self):
        self.workflow = StateGraph(CustomStateModel)
        self.graph = None
        self.llm = llmInstance()
        self.tools = getTools()
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.memory = MemorySaver()

    def compile_graph(self):
        """
        Compile the graph and add edges between nodes
        """
        self.workflow.add_node("tools",self.tooling())
        self.workflow.add_node("internalSearch", self.internalSearch()) 
        self.workflow.add_node("grade_documents", call_mcp_server(MCP_TOOLS_SERVICE_ALIASES['documentGrader']))
        self.workflow.add_node("responseGenerator", call_mcp_server(MCP_TOOLS_SERVICE_ALIASES['responseGenerator']))
        # Build graph
        self.workflow.set_conditional_entry_point(
            call_mcp_server(MCP_TOOLS_SERVICE_ALIASES['router']),
            {
                "tools": "tools",
                "internalSearch": "internalSearch",
            },
        )
        self.workflow.add_edge("tools", "responseGenerator")
        self.workflow.add_edge("internalSearch", "grade_documents")
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
            call_mcp_server(MCP_TOOLS_SERVICE_ALIASES['hallucinationGrader']),
            {
                "not supported": "responseGenerator",
                "useful": END,
                "not useful": "websearch",
                "max retries": END,
            },
        )
        self.graph = self.workflow.compile(checkpointer=self.memory)
        return self.graph


    def display_graph(self):
        """
        Display the graph using IPython display
        """
        # self.graph.render("graph", format="png")
        display(Image(self.graph.get_graph().draw_mermaid_png()))
    
    def tooling(self) -> ToolNode:
        """ 
        Returns a ToolNode with the tools to be used in the graph.
        """
        return ToolNode(tools=[self.tools])
    
    def internalSearch(self):
        """
        Returns the VectorDB Search with our own documents stored in the vector database.
        """
        return 
        