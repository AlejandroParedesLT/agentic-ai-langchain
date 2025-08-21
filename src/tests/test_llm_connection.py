import subprocess
import json
from langchain_ollama import ChatOllama

class llmservice:
    def __init__(self,
                  model_id: str,
                  format:str = '', 
                  temperature: float = 0.0, 
                  max_tokens: int = 256):
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.model = ChatOllama(model=model_id, temperature=temperature,format=format, base_url="http://127.0.0.1:11434")

    def start(self):
        # Check if the model is already running
        try:
            result = subprocess.run(["ollama", "status"], capture_output=True, text=True)
            if "not running" in result.stdout:
                # Start the model if it's not running
                subprocess.run(["ollama", "start", self.model_id], check=True)
                print(f"Model {self.model_id} started successfully.")
        except Exception as e:
            print(f"Error starting model: {e}")

    def invoke(self, prompt: str) -> str:
        # Call the model with the prompt and get the response
        try:
            print(f"Invoking model with prompt: {prompt}")
            response = self.model.invoke(prompt)
            print(f"Model response: {response}")
            return response
        except Exception as e:
            print(f"Error invoking model: {e}")
            return None

if __name__ == "__main__":
    # Example usage
    llm = llmservice(model_id="llama3.2:3b-instruct-fp16", temperature=0.0, format="json")
    # llm.start()
    # res=subprocess.run(["ls"], capture_output=True, text=True)
    # print(res.stdout)
    from langchain_core.messages import HumanMessage, SystemMessage
    from src.agents.router import router_instructions
    route_question = llm.invoke(
        [SystemMessage(content=router_instructions)]
        + [HumanMessage(content="What is agentic AI and how is it used in modern devices?")]
    )
    print(route_question)