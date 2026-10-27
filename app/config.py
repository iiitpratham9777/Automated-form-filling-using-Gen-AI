from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
    database_url:str="sqlite+aiosqlite:///./formpilot.db"; jwt_secret:str="change-me"; jwt_algorithm:str="HS256"; access_token_expire_minutes:int=60; storage_dir:str="./storage"; max_upload_mb:int=25; demo_form_url:str="http://localhost:3000"; llm_provider:str="none"; openai_api_key:str=""
@lru_cache
def get_settings(): return Settings()
