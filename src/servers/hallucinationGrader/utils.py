from langchain_core.messages import HumanMessage, SystemMessage
from src.servers.hallucinationGrader.model import hallucinationGraderInput, hallucinationGraderOutput
import json
from src.models.ollama import llmservice

from src.agents.hallucination_grader import (
    hallucination_grader_instructions,
    hallucination_grader_prompt,
    answer_grader_instructions,
    answer_grader_prompt)

# Post-processing
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs if doc.page_content)

def gradeAnswer(input: hallucinationGraderInput, llm_json_mode:llmservice):
    """
    Determines whether the generation is grounded in the document and answers question

    Args:
        input: The current graph state

    Returns:
        str: Decision for next node to call
    """

    print("---CHECK HALLUCINATIONS---")
    question = input.question
    documents = input.documents
    generation = input.generation
    max_retries = 3

    hallucination_grader_prompt_formatted = hallucination_grader_prompt.format(
        documents=format_docs(documents), generation=generation.content
    )
    print('Hallucination grader prompt: ',hallucination_grader_prompt_formatted)
    print('Hallucination grader instructions: ',hallucination_grader_instructions)
    result = llm_json_mode.invoke(
        [SystemMessage(content=hallucination_grader_instructions)]
        + [HumanMessage(content=hallucination_grader_prompt_formatted)]
    )
    print('Hallucination grader results', result)
    
    grade = json.loads(result.content)["binary_score"]

    # Check hallucination
    if grade == "yes":
        print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        # Check question-answering
        print("---GRADE GENERATION vs QUESTION---")
        # Test using question and generation from above
        print('The generation is as follows: ',generation.content)
        answer_grader_prompt_formatted = answer_grader_prompt.format(
            question=question, generation=generation.content
        )
        result = llm_json_mode.invoke(
            [SystemMessage(content=answer_grader_instructions)]
            + [HumanMessage(content=answer_grader_prompt_formatted)]
        )
        print('The generation is as follows: ',result)
        grade = json.loads(result.content)["binary_score"]
        if grade == "yes":
            print("---DECISION: GENERATION ADDRESSES QUESTION---")
            return hallucinationGraderOutput(result="useful")
        elif input.steps <= max_retries:
            print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            return hallucinationGraderOutput(result="not useful")
        else:
            print("---DECISION: MAX RETRIES REACHED---")
            return hallucinationGraderOutput(result="max retries")
    elif input.steps <= max_retries:
        print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
        return hallucinationGraderOutput(result="not supported")
    else:
        print("---DECISION: MAX RETRIES REACHED---")
        return hallucinationGraderOutput(result="max retries")