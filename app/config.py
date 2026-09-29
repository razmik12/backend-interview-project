from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    db_psw: str = Field(alias="POSTGRES_PASSWORD")
    db_user: str = Field(alias="POSTGRES_USER")
    db_name: str = Field(alias="POSTGRES_DB")
    secret_key:str = Field(alias="SECRET_KEY")
    algorithm:str = Field(alias="ALGORITHM")
    access_exp:int = Field(alias="access_token_expire_minutes")
    refresh_exp:int = Field(alias="refresh_token_expire_days")
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_psw}@postgres:5432/{self.db_name}"



def get_settings() -> Settings:
    return Settings()

settings = get_settings()
    
