import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
load_dotenv()
from typing import Annotated
from langgraph.graph import END
from langchain_tavily import TavilySearch
from typing_extensions import TypedDict
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class State(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatOllama(model="llama3.2:3b-instruct-fp16", temperature=0.0, format="", max_tokens=512)

os.environ["TAVILY_API_KEY"] = "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"
tool = TavilySearch(max_results=2)
# tools = [tool]
# llm = llm.bind_tools([tool])

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

tool_node = ToolNode(tools=[tool])

graph_builder = StateGraph(State)

# add nodes as before
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)
graph_builder.set_entry_point("chatbot")

# here’s the fixed conditional edge:
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
    ["tools", END]    # <-- explicitly list your tool node and the END
)

# continue as before
graph_builder.add_edge("tools", "chatbot")
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

from IPython.display import Image, display

try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass

png_data = graph.get_graph().draw_mermaid_png()
with open("output.png", "wb") as f:
    f.write(png_data)

# Convert string messages to proper message objects
messages = {
    "messages": [
        SystemMessage(content="You are a helpful assistant that uses Tavily to search the web. The user will ask you to search for something. If need to use a tool, respond with 'tool'. If you can answer the question, respond with 'end'."),
        HumanMessage(content="Search for the best restaurant in Seattle today.")
    ]
}

# You can also increase the recursion limit if needed
custom_config = {
    "configurable": {"thread_id": "1"},
}

response = graph.invoke(
    messages,
    custom_config
)

print(response)


snapshot = graph.get_state(custom_config)
print(snapshot)

# Convert string messages to proper message objects
messages = {
    "messages": [
        SystemMessage(content="You are a helpful assistant that uses Tavily to search the web. The user will ask you to search for something. If need to use a tool, respond with 'tool'. If you can answer the question, respond with 'end'."),
        HumanMessage(content="What was the top 1 restaurant you suggested in the last search?"),
    ]
}



response = graph.invoke(
    messages,  # first argument
    custom_config     # second argument
)

print(response)

snapshot = graph.get_state(custom_config)
print(snapshot)
