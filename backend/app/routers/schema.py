from pydantic import BaseModel
from typing import Optional, List


class ChatRequest(BaseModel):
    message: str
    chat_history: Optional[List[dict]] = None
    model_type: Optional[str] = "openai"
    temperature: Optional[float] = 0.2

class ChatResponse(BaseModel):
    response: str
    chat_history: List[dict]

class HealthCheck(BaseModel):
    status: str = "OK"

class ChatbotSettings(BaseModel):
    model_type: str
    temperature: float
    max_tokens: int
    top_p: float