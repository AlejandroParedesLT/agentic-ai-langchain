from langchain_core.messages import HumanMessage, SystemMessage
import json
# from src.servers.routers.main import llm_json_mode
# from src.servers.router.model import RouterOutput, RouterInput
# from src.agents.router import router_instructions
# from src.models.ollama import llmservice

from model import RouterOutput, RouterInput
from agents import router_instructions
from langchain_ollama import ChatOllama


def route_question(input:RouterInput, llm_json_mode:ChatOllama) -> RouterOutput:
    """
    Route question to web search or RAG

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """

    print("---ROUTE QUESTION---")
    # print(f"Methods: {dir(llm_json_mode)}")
    route_question = llm_json_mode.invoke(
        [SystemMessage(content=router_instructions)]
        + [HumanMessage(content=input.input)]
    )
    print(f"Route question: {route_question}")
    source = json.loads(route_question.content)["datasource"]
    print(f"Route question source: {source}")
    if source == "websearch":
        print("---ROUTE QUESTION TO WEB SEARCH---")
        return RouterOutput(output="websearch")
    elif source == "vectordb":
        print("---ROUTE QUESTION TO RAG---")
        return RouterOutput(output="vectordb")