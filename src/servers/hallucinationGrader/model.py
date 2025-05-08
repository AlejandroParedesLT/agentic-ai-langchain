from pydantic import BaseModel
from typing import Literal, List
from langchain.schema import Document
from typing import Dict

class hallucinationGraderInput(BaseModel):
    question: str
    documents: List[Document]
    generation: str
    steps: int

class hallucinationGraderOutput(BaseModel):
    result: Dict

