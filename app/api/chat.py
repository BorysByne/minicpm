from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.minicpm_service import minicpm_service

router = APIRouter()

@router.post("/chat/completions", response_model=ChatResponse)
async def chat_completion(request: ChatRequest):
    try:
        return await minicpm_service.process_chat_request(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/model-info")
async def get_model_info():
    try:
        return await minicpm_service.get_model_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))