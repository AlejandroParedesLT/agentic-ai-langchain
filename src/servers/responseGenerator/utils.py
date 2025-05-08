from langchain_core.messages import HumanMessage, SystemMessage
from src.agents.generator import rag_prompt
from src.servers.responseGenerator.model import GeneratorResponseInput, GeneratorResponseOutput
from src.models.ollama import llmservice

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs if doc.page_content)

def generate(input:GeneratorResponseInput, llm:llmservice)->GeneratorResponseOutput:
    """
    Generate answer using RAG on retrieved documents

    Args:
        A doc, the question and the initial response from the LLM

    Returns:
        Generated response with the number of steps.
    """
    print("---GENERATE---")
    # RAG generation
    docs_txt = format_docs(input.documents)
    rag_prompt_formatted = rag_prompt.format(context=docs_txt, question=input.question)
    generation = llm.invoke([HumanMessage(content=rag_prompt_formatted)])
    return GeneratorResponseOutput(output=generation, steps=input.steps)