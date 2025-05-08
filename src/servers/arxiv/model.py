from pydantic import BaseModel

class ArxivInput(BaseModel):
    input: str  # Either a string or doi

class ArxivOutput(BaseModel):
    output: str

