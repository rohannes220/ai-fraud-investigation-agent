from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
    database_url:str
    openai_api_key:str=""
    openai_chat_model:str="gpt-4.1-mini"
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
settings=Settings()
