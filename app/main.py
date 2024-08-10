import uvicorn
from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.core.config import get_settings, Settings
from app.models.minicpm import load_model, get_model

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    settings = get_settings()
    print(f"Current model: {settings.minicpm_model_name}")
    load_model(settings.minicpm_model_name)
    model = get_model()
    print(f"Running on device: {model.device}")


app.include_router(chat_router, prefix="/v1")


def get_model_choice():
    print("\nPlease choose the MiniCPM model version:")
    print("1. openbmb/MiniCPM-V-2_6-int4 (Quantized version)")
    print("   - Faster inference")
    print("   - Lower memory usage")
    print("   - Slight reduction in accuracy")
    print("\n2. openbmb/MiniCPM-V-2_6 (Full version)")
    print("   - Higher accuracy")
    print("   - Higher memory usage")
    print("   - Slower inference")

    while True:
        choice = input("\nEnter your choice (1 or 2): ").strip()
        if choice in ['1', '2']:
            return "int4" if choice == '1' else "full"
        else:
            print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    settings = get_settings()
    model_choice = get_model_choice()

    settings.minicpm_model_name = "openbmb/MiniCPM-V-2_6-int4" if model_choice == "int4" else "openbmb/MiniCPM-V-2_6"
    print(f"\nSelected model: {settings.minicpm_model_name}")

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)