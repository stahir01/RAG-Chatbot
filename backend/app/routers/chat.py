from fastapi import APIRouter, HTTPException
from backend.app.modules.chatbot_logic import Chatbot
from backend.app.routers.schema import ChatRequest, ChatResponse, HealthCheck, ChatbotSettings
from typing import Optional

router = APIRouter()

chatbot = Chatbot()

@router.get("/health", response_model=HealthCheck)
async def health_check():
    return {"status": "OK"}

@router.post("/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    try:
        if request.model_type or request.temperature:
            chatbot.model_type = request.model_type or chatbot.model_type
            chatbot.temperature = request.temperature or chatbot.temperature
        
        response = chatbot.generate_text(request.message)
        
        chat_history = [
            {"role": "user", "content": request.message},
            {"role": "assistant", "content": response}
        ]
        
        return {
            "response": response,
            "chat_history": chat_history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset")
async def reset_chat():
    try:
        chatbot.clear_history()
        return {"message": "Chat history cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/settings", response_model=ChatbotSettings)
async def get_settings():
    return {
        "model_type": chatbot.model_type,
        "temperature": chatbot.temperature,
        "max_tokens": chatbot.max_tokens,
        "top_p": chatbot.top_p
    }

@router.put("/settings")
async def update_settings(settings: ChatbotSettings):
    try:
        chatbot.model_type = settings.model_type
        chatbot.temperature = settings.temperature
        chatbot.max_tokens = settings.max_tokens
        chatbot.top_p = settings.top_p
        return {"message": "Settings updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))