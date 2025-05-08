from langchain_core.messages import HumanMessage, SystemMessage
import json
# from src.servers.routers.main import llm_json_mode
from src.servers.routers.model import RouterOutput, RouterInput
from src.agents.router import router_instructions
from src.models.ollama import llmservice


def route_question(input:RouterInput, llm_json_mode:llmservice):
    """
    Route question to web search or RAG

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """

    print("---ROUTE QUESTION---")
    route_question = llm_json_mode.invoke(
        [SystemMessage(content=router_instructions)]
        + [HumanMessage(content=input.prompt)]
    )
    source = json.loads(route_question.content)["datasource"]
    if source == "websearch":
        print("---ROUTE QUESTION TO WEB SEARCH---")
        return RouterOutput(result="websearch")
    elif source == "vectorstore":
        print("---ROUTE QUESTION TO RAG---")
        return RouterOutput(result="vectorstore")