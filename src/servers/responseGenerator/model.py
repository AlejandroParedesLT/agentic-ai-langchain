from pydantic import BaseModel
# from typing import Literal, List
# from langchain.schema import Document
from typing import Any 
from typing import Optional


class GeneratorResponseInput(BaseModel):
    context: Optional[Any] = None
    question: str
    steps: int
class GeneratorResponseOutput(BaseModel):
    output: str
    steps: int