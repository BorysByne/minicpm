from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    minicpm_model_name: str = "openbmb/MiniCPM-V-2_6-int4"

    class Config:
        env_file = ".env"
        protected_namespaces = ()

@lru_cache()
def get_settings():
    return Settings()