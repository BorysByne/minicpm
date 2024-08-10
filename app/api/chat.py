from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse, Choice, ResponseMessage, ErrorResponse
from app.models.minicpm import get_model
import uuid

router = APIRouter()

@router.post("/chat/completions", response_model=ChatResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def chat_completion(request: ChatRequest):
    try:
        model = get_model()
        response_content = model.chat(
            msgs=request.messages,
            temperature=request.temperature,
            seed=request.seed,
            max_tokens=request.max_tokens
        )
        
        choice = Choice(
            finish_reason="stop",  # Assume it stopped naturally; adjust as needed
            index=0,
            message=ResponseMessage(
                content=response_content,
                role="assistant",
                refusal=None,
                tool_calls=None,
                function_call=None
            ),
            logprobs=None
        )
        
        return ChatResponse(
            id=str(uuid.uuid4()),
            choices=[choice],
            model=request.model
        )
    except ValueError as ve:
        # Handle the case of multiple system messages
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Handle other exceptions
        raise HTTPException(status_code=500, detail=str(e))
        
@router.get("/model-info")
async def get_model_info():
    try:
        return await minicpm_service.get_model_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
