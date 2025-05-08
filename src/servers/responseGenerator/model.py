from pydantic import BaseModel
# from typing import Literal, List
# from langchain.schema import Document
from typing import Any 

class GeneratorResponseInput(BaseModel):
    context: Any #List[Document]
    question: str
    steps: int
class GeneratorResponseOutput(BaseModel):
    output: str
    steps: int