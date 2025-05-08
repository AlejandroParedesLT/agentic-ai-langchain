from pydantic import BaseModel

class WebSearchInput(BaseModel):
    input: str  # summary from loan_parser

class WebSearchOutput(BaseModel):
    output: str