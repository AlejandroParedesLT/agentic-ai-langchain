from pydantic import BaseModel
from typing import Literal

class RouterInput(BaseModel):
    input: str  # summary from loan_parser

class RouterOutput(BaseModel):
    output: Literal["websearch", "vectordb", "coding", "arxiv", "dataAnalysis"]
