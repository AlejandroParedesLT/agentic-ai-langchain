from fastapi import FastAPI, Depends, HTTPException
import os
import sys
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
# from src.graph.pipeline.flow_graph_test import  CustomLangGraph
# from src.graph.models.model import ChatRequest, ChatResponse, Message

from pipeline.flow_graph_test import  CustomLangGraph
from models.model import ChatRequest, ChatResponse, Message

from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Fast API internall
app = FastAPI(title="LangGraph API", description="API for LangGraph-based chatbot with tools")

instance_graph = CustomLangGraph() 
comp_graph = instance_graph.compile_graph()
print(type(instance_graph))
print("Graph compiled")

def instanceGraph():
    return instance_graph.graph
# Models for API
@app.post("/generate", response_model=ChatResponse)
async def generate(
    request: ChatRequest,
    lang_graph = Depends(instanceGraph)
    ) -> ChatResponse:
    """Process a web search request."""
    # TODO: Dynamically check for the config creating in DB a new config if necessary
    try:
        # Convert API messages to LangChain message format
        lang_chain_messages = []
        for msg in request.messages:
            if msg.role == "user":
                lang_chain_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                lang_chain_messages.append(AIMessage(content=msg.content))
            elif msg.role == "system":
                lang_chain_messages.append(SystemMessage(content=msg.content))
        print("Message from main:", lang_chain_messages)
         # Prepare state for graph
        state = {"messages": lang_chain_messages, "max_retries": 3, "loop_step": 0, "tools_results": {}}
        print("State from main:", state)
        
        ###############################
        # Test
        # print("Test graph from main")
        # messages = {
        #     "messages": [
        #         SystemMessage(content="You are a helpful assistant that uses Tavily to search the web. The user will ask you to search for something. If need to use a tool, respond with 'tool'. If you can answer the question, respond with 'end'."),
        #         HumanMessage(content="Search for the best restaurant in Seattle today.")
        #     ]
        # }
        
        # response = instance_graph.graph.invoke(messages,config) #.graph.invoke(messages, config)
        # print(response)

        print("Graph from main")
        # Invoke graph
        # result = await lang_graph.ainvoke(state, config)
        config = {"configurable": {"thread_id": "1"}}
        result = lang_graph.invoke(state, config)
        print("Result from main:", result)

        snapshot = lang_graph.get_state(config)
        print(snapshot)

        # Extract messages from result
        output_messages = []
        for msg in result["messages"]:
            if isinstance(msg, HumanMessage):
                output_messages.append(Message(role="user", content=msg.content))
            elif isinstance(msg, AIMessage):
                output_messages.append(Message(role="assistant", content=msg.content))
            elif isinstance(msg, SystemMessage):
                output_messages.append(Message(role="system", content=msg.content))
        
        return ChatResponse(messages=output_messages)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)