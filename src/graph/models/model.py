from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# Models for API
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    messages: List[Message]