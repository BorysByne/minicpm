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

class ToolCall(BaseModel):
    id: str
    type: str
    function: Dict[str, str]

class ResponseMessage(BaseModel):
    content: Optional[str]
    refusal: Optional[str]
    tool_calls: Optional[List[ToolCall]]
    role: str
    function_call: Optional[Dict[str, str]]

class LogProbs(BaseModel):
    content: Optional[List[Dict[str, Union[str, float]]]]

class Choice(BaseModel):
    finish_reason: str
    index: int
    message: ResponseMessage
    logprobs: Optional[LogProbs]

class ChatResponse(BaseModel):
    id: str
    choices: List[Choice]
    model: str

class ErrorResponse(BaseModel):
    detail: str