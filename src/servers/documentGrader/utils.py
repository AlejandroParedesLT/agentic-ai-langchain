from src.agents.retrievalGrader import doc_grader_instructions, doc_grader_prompt
from langchain_core.messages import HumanMessage, SystemMessage
from src.servers.documentGrader.model import GraderInput, GraderOutput
from src.models.ollama import llmservice
import json

def grade_documents(input:GraderInput, llm:llmservice):
    """
    Determines whether the retrieved documents are relevant to the question
    If any document is not relevant, we will set a flag to run web search

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Filtered out irrelevant documents and updated web_search state
    """

    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")

    # Score each doc
    filtered_docs = []
    web_search = "No"
    for d in input.documents:
        doc_grader_prompt_formatted = doc_grader_instructions.format(
            document=d.page_content, question=input.prompt
        )
        result = llm.invoke(
            [SystemMessage(content=doc_grader_prompt)]
            + [HumanMessage(content=doc_grader_prompt_formatted)]
        )
        grade = json.loads(result.content)["binary_score"]
        # Document relevant
        if grade.lower() == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_docs.append(d)
        # Document not relevant
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")
            # We do not include the document in filtered_docs
            # We set a flag to indicate that we want to run web search
            web_search = "Yes"
            continue
    return GraderOutput(documents=filtered_docs,web_search=web_search)