from pydantic import BaseModel
from typing import Dict, Optional, List
from langchain.schema import Document

class GraderInput(BaseModel):
    prompt: str
    documents: List[Document]

class GraderOutput(BaseModel):
    documents: List[Document]
    web_search: str