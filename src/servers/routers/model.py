from pydantic import BaseModel
from typing import Literal

class RouterInput(BaseModel):
    prompt: str  # summary from loan_parser

class RouterOutput(BaseModel):
    result: Literal["websearch", "vectorstore"]