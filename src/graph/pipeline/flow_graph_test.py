import operator
from typing import List, Annotated
from langgraph.graph import StateGraph
from IPython.display import Image, display
from typing_extensions import TypedDict
from typing import List, Annotated, Dict, Any
from langchain_ollama import ChatOllama
# from src.graph.utils.langLambdas import decide_to_generate

import httpx
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph
from langgraph.graph import END
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langchain_core.tools import Tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


import os
load_dotenv()

MCP_TOOLS_SERVICE_ALIASES ={
    "arxiv": os.getenv('arxiv', "http://host.docker.internal:8011/process"),
    "calculator": os.getenv('calculator', "http://host.docker.internal:8001/process"),
}

def llmInstance()->ChatOllama:
    print("llmInstance, connected")
    print("This is the env for the llm: ",os.getenv('LLM_ID'))
    llm_json_mode = ChatOllama(model=str(os.getenv("LLM_ID")), temperature=float(os.getenv('LLM_TEMPERATURE')), format=str(os.getenv('LLM_format')), base_url="http://host.docker.internal:11434")
    return llm_json_mode

def call_tool(tool_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Call a tool service and return the result"""
    if tool_name not in MCP_TOOLS_SERVICE_ALIASES:
        return {"error": f"Tool {tool_name} not found"}
    
    try:
        response = httpx.post(MCP_TOOLS_SERVICE_ALIASES[tool_name], json=input_data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Error calling {tool_name}: {str(e)}"}

def setup_tools() -> List[Tool]:
    """Setup tool definitions for LangChain tools"""
    tools = []
    
    # Arxiv Search Tool
    tools.append(
        Tool(
            name="arxiv",
            description="Search academic papers on Arxiv. Provide a query string to search for papers or DOI preferred.",
            func=lambda query: call_tool("arxiv", {"input": query})
        )
    )
    
    # Calculator Tool
    tools.append(
        Tool(
            name="calculator",
            description="Return the result of a mathematical expressions (example '1+2' returns 3). Provide a string expression to calculate.",
            func=lambda expression: call_tool("calculator", {"input": expression})
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
    tools_results: Dict[str, Any] # Web search result

# class ServerState(TypedDict):
#     """
#     Intermediate state for the server.
#     """
#     payload: Any

# def call_mcp_server(url):
#     async def fn(state: ServerState) -> ServerState:
#         print(f"[DEBUG] Calling {url} with payload:", state["payload"])
#         async with httpx.AsyncClient() as client:
#             response = await client.post(url, json=state["payload"])
#             response.raise_for_status()
#             return {"payload": response.json()}
#     return RunnableLambda(fn).with_config({"run_name": f"CallMCP::{url.split(':')[2]}"})

def analyze_query_for_tools(state: CustomStateModel) -> str:
    """Analyze the latest message to determine if tools are needed"""
    messages = state["messages"]
    if not messages:
        return "chatbot"
    
    last_message = messages[-1]
    if not isinstance(last_message, HumanMessage):
        return "chatbot"
    
    # Check if query likely needs arxiv
    if any(term in last_message.content.lower() for term in ["paper", "arxiv", "research", "academic", "journal"]):
        return "tools"
    
    # Check if query likely needs calculator
    if any(term in last_message.content.lower() for term in ["calculate", "compute", "math", "equation", "formula"]):
        return "tools"
    
    # Default to chatbot
    return "chatbot"


class CustomLangGraph:
    def __init__(self):
        self.workflow = StateGraph(CustomStateModel)
        self.graph = None
        self.llm = llmInstance()
        self.tools = setup_tools()
        # self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.memory = MemorySaver()

    def compile_graph(self):
        """
        Compile the graph and add edges between nodes
        """
        
        self.workflow.add_node("tools",self.tooling())
        self.workflow.add_node("chatbot", self.chatbot)
        self.workflow.add_node("process_tool_results", self.process_tool_results)
        self.workflow.set_conditional_entry_point( 
            analyze_query_for_tools,  # routing function
            {
                "tools": "tools",  # mapping from function output to node name
                "chatbot": "chatbot"
            }
        )
        # self.workflow.set_entry_point("chatbot")
        self.workflow.add_edge("tools", "process_tool_results")
        self.workflow.add_edge("process_tool_results", END)
        self.workflow.add_edge("chatbot", END)

        self.graph = self.workflow.compile(checkpointer=self.memory)
        return self.graph


    def display_graph(self):
        """
        Display the graph using IPython display
        """
        # self.graph.render("graph", format="png")
        display(Image(self.graph.get_graph().draw_mermaid_png()))
    
    def tooling(self):
        """Tool handling node"""
        from utils.router_agent import router_instructions
        def _run_tools(state: CustomStateModel):
            messages = state["messages"]
            
            # Use LLM to decide which tool to use and what input to provide
            tool_selection_prompt = SystemMessage(content=router_instructions)
            
            # Get the last human message
            last_message = next((m for m in reversed(messages) if isinstance(m, HumanMessage)), None)
            if not last_message:
                return {"messages": messages}
            
            # Call LLM to decide on tool
            tool_decision = self.llm.invoke([tool_selection_prompt, last_message])
            
            # Parse the tool name and input from LLM's output
            import json
            try:
                content = tool_decision.content
                # Extract JSON if it's embedded in markdown code blocks
                # if "```json" in content:
                #     content = content.split("```json")[1].split("```")[0].strip()
                # elif "```" in content:
                #     content = content.split("```")[1].split("```")[0].strip()
                
                tool_info = json.loads(content)
                tool_name = tool_info.get("tool")
                tool_input = tool_info.get("input")
                
                # Find the matching tool
                selected_tool = next((t for t in self.tools if t.name == tool_name), None)
                
                if selected_tool:
                    # Call the tool
                    tool_result = selected_tool.invoke(tool_input)
                    
                    # Add result to state
                    return {
                        "messages": messages,
                        "tools_results": {
                            "tool": tool_name,
                            "input": tool_input,
                            "result": tool_result
                        }
                    }
            except Exception as e:
                print(f"Error processing tool: {e}")
            
            # If anything fails, continue without tool results
            return {"messages": messages}
        
        return RunnableLambda(_run_tools)
    
    def chat(self):
        """
        Returns the VectorDB Search with our own documents stored in the vector database.
        """
        print("Chatbot invoked")
        return {"messages": [self.llm.invoke(self.state["messages"])]} 
    
    # def analyze_query_for_tools(self):
    #     """Analyze the latest message to determine if tools are needed"""
    #     messages = self.state["messages"]
    #     if not messages:
    #         return "chatbot"
        
    #     last_message = messages[-1]
    #     if not isinstance(last_message, HumanMessage):
    #         return "chatbot"
        
    #     # Check if query likely needs arxiv
    #     if any(term in last_message.content.lower() for term in ["paper", "arxiv", "research", "academic", "journal"]):
    #         return "tools"
        
    #     # Check if query likely needs calculator
    #     if any(term in last_message.content.lower() for term in ["calculate", "compute", "math", "equation", "formula"]):
    #         return "tools"
        
    #     # Default to chatbot
    #     return "chatbot"
    def process_tool_results(self, state: CustomStateModel):
        """Process tool results and generate response"""
        def _process_results(state: CustomStateModel):
            messages = state["messages"]
            tool_results = state.get("tools_results", {})
            
            if not tool_results:
                return {"messages": messages}
            
            # Prepare system message with tool results context
            system_prompt = SystemMessage(content="""
            You are a helpful assistant. You have access to external tools.
            Respond to the user's query using the results from the tool that was just called.
            Explain what tool was used and how the information helps answer their question.
            """)
            
            # Format tool results for LLM consumption
            tool_name = tool_results.get("tool", "unknown")
            tool_input = tool_results.get("input", "")
            tool_result = tool_results.get("result", {})
            
            tool_info = f"""
            Tool Used: {tool_name}
            Tool Input: {tool_input}
            Tool Result: {tool_result}
            """
            
            # Get the last human message
            last_message = next((m for m in reversed(messages) if isinstance(m, HumanMessage)), None)
            if not last_message:
                return {"messages": messages}
            
            # Generate response using tool results
            response = self.llm.invoke([
                system_prompt,
                HumanMessage(content=f"User query: {last_message.content}\n\n{tool_info}")
            ])
            
            # Add AI message to conversation
            updated_messages = messages + [AIMessage(content=response.content)]
            
            return {"messages": updated_messages}
        
        return RunnableLambda(_process_results)
    
    # def chat(self, state):
    #     """Handle normal chat without tools"""
    #     def _chat(state: CustomStateModel):
    #         messages = state["messages"]
    #         response = self.llm.invoke(messages)
    #         updated_messages = messages + [response]
    #         return {"messages": updated_messages}
        
    #     return RunnableLambda(_chat)

    def chatbot(self, state: CustomStateModel):
        
        return {"messages": [self.llm.invoke(state["messages"])]}
        
    # async def ainvoke(self, state, config=None):
    #     """Async invoke for the graph"""
    #     if not self.graph:
    #         self.compile_graph()
            
    #     # If state payload contains messages, extract them
    #     if isinstance(state, dict) and "payload" in state:
    #         payload = state["payload"]
    #         if isinstance(payload, dict) and "messages" in payload:
    #             messages = payload["messages"]
    #             state = {"messages": messages, "max_retries": 3, "loop_step": 0, "conversation": [], "tools_results": {}}
    #         else:
    #             # Handle case where payload doesn't contain messages
    #             state = {"messages": [HumanMessage(content=str(payload))], "max_retries": 3, "loop_step": 0, "conversation": [], "tools_results": {}}
        
    #     result = await self.graph.ainvoke(state, config)
        
    #     # Format the result for the API response
    #     return {"payload": {"messages": result["messages"]}}

# if __name__ == "__main__":
graph_instance = CustomLangGraph()
graph_instance.compile_graph()
dev_ = graph_instance.graph