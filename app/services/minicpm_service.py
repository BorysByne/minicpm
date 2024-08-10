from typing import List, Dict, Any, Optional
from app.models.minicpm import get_model
from app.schemas.chat import ChatRequest, ChatResponse

class MiniCPMService:
    @staticmethod
    async def process_chat_request(request: ChatRequest) -> ChatResponse:
        """
        Process a chat request using the MiniCPM model.

        Args:
            request (ChatRequest): The chat request containing messages and parameters.

        Returns:
            ChatResponse: The model's response wrapped in a ChatResponse object.

        Raises:
            RuntimeError: If there's an error processing the request.
        """
        try:
            model = get_model()
            response = model.chat(
                msgs=request.messages,
                temperature=request.temperature,
                seed=request.seed,
                max_tokens=request.max_tokens
            )
            return ChatResponse(model=model.model_name, response=response)
        except Exception as e:
            raise RuntimeError(f"Error processing chat request: {str(e)}")

    @staticmethod
    async def get_model_info() -> Dict[str, Any]:
        """
        Get information about the currently loaded model.

        Returns:
            Dict[str, Any]: A dictionary containing model information.
        """
        model = get_model()
        return {
            "model_name": model.model_name,
            "device": str(model.device),
            "is_quantized": "int4" in model.model_name
        }

minicpm_service = MiniCPMService()