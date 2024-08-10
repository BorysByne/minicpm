from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.models.minicpm import get_model
from app.services.minicpm_service import minicpm_service

router = APIRouter()

@router.post("/chat/completions", response_model=ChatResponse)
async def chat_completion(request: ChatRequest):
    try:
        print(request.messages)
        model = get_model()
        response = model.chat(
            msgs=request.messages,
            temperature=request.temperature,
            seed=request.seed,
            max_tokens=request.max_tokens
        )
        return ChatResponse(model=request.model, response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/model-info")
async def get_model_info():
    try:
        return await minicpm_service.get_model_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))