from pydantic import BaseModel, Field
from typing import List, Dict, Union, Optional

class MessageContent(BaseModel):
    type: str
    text: Optional[str] = None
    image_url: Optional[Dict[str, str]] = None

class Message(BaseModel):
    role: str
    content: Union[str, List[MessageContent]]

class ResponseFormat(BaseModel):
    type: str = "json_object"

class ChatRequest(BaseModel):
    model: str
    temperature: float = Field(0, ge=0, le=2)
    messages: List[Message]
    seed: Optional[int] = None
    response_format: ResponseFormat = ResponseFormat()
    max_tokens: int = Field(4095, ge=1, le=8192)

class ChatResponse(BaseModel):
    model: str
    response: str