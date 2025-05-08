from pydantic import BaseModel

class CalculatorInput(BaseModel):
    input: str

class CalculatorOutput(BaseModel):
    output: str