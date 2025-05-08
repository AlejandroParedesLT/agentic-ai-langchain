from pydantic import BaseModel

class CodingInput(BaseModel):
    input: str  # summary from loan_parser

class CodingOutput(BaseModel):
    output: str