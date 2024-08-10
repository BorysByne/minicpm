import torch
import io
import base64
from typing import List, Dict, Any, Optional
from PIL import Image
from transformers import AutoModel, AutoTokenizer


class MiniCPM:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.device = self._get_device()
        self.load_model()

    def _get_device(self) -> torch.device:
        """Determine the available device for computation."""
        if torch.cuda.is_available():
            return torch.device("cuda")
        elif torch.backends.mps.is_available():
            return torch.device("mps")
        else:
            return torch.device("cpu")

    def load_model(self):
        """Load the MiniCPM model and tokenizer."""
        try:
            print(f"Loading model on {self.device}")
            if "int4" in self.model_name:
                self.model = AutoModel.from_pretrained(self.model_name, trust_remote_code=True)
            else:
                if self.device.type == "cuda":
                    self.model = AutoModel.from_pretrained(
                        self.model_name,
                        trust_remote_code=True,
                        attn_implementation='sdpa',
                        torch_dtype=torch.bfloat16
                    ).eval().to(self.device)
                elif self.device.type == "mps":
                    self.model = AutoModel.from_pretrained(
                        self.model_name,
                        trust_remote_code=True,
                        attn_implementation='eager',  # MPS doesn't support sdpa
                        torch_dtype=torch.float32  # MPS doesn't support bfloat16
                    ).eval().to(self.device)
                else:  # CPU
                    self.model = AutoModel.from_pretrained(
                        self.model_name,
                        trust_remote_code=True,
                        attn_implementation='eager',
                        torch_dtype=torch.float32
                    ).eval()

            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_code=True)
            print(f"Model loaded successfully on {self.device}")
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")

    def chat(self, msgs: List[Dict[str, Any]], temperature: float = 0, seed: Optional[int] = None,
             max_tokens: int = 4095) -> str:
        """
        Process a chat request using the MiniCPM model.

        Args:
            msgs (List[Dict[str, Any]]): List of message dictionaries.
            temperature (float): Sampling temperature.
            seed (Optional[int]): Random seed for reproducibility.
            max_tokens (int): Maximum number of tokens to generate.

        Returns:
            str: The model's response.
        """
        try:
            # Process images in the messages
            processed_msgs = []
            for msg in msgs:
                if isinstance(msg['content'], list):
                    processed_content = []
                    for item in msg['content']:
                        if item['type'] == 'image_url':
                            # Convert base64 to PIL Image
                            image_data = item['image_url']['url'].split(',')[1]
                            image = Image.open(io.BytesIO(base64.b64decode(image_data))).convert('RGB')
                            processed_content.append(image)
                        else:
                            processed_content.append(item['text'])
                    msg['content'] = processed_content
                processed_msgs.append(msg)

            # Set random seed if provided
            if seed is not None:
                torch.manual_seed(seed)
                if self.device.type == "cuda":
                    torch.cuda.manual_seed(seed)

            with torch.no_grad():
                response = self.model.chat(
                    image=None,
                    msgs=processed_msgs,
                    tokenizer=self.tokenizer,
                    temperature=temperature,
                    max_new_tokens=max_tokens
                )
            return response
        except Exception as e:
            raise RuntimeError(f"Chat processing failed: {e}")


model_instance = None


def load_model(model_name: str):
    global model_instance
    model_instance = MiniCPM(model_name)


def get_model() -> MiniCPM:
    if model_instance is None:
        raise RuntimeError("Model not initialized. Call load_model first.")
    return model_instance