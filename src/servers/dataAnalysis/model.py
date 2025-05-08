from pydantic import BaseModel
from typing import Dict
from typing import Union

class DataAnalysisInput(BaseModel):
    input: Union[str, None]

class DataAnalysisOutput(BaseModel):
    output: Dict