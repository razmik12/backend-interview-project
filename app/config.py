from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_psw: str = Field(alias="POSTGRES_PASSWORD")
    db_user: str = Field(alias="POSTGRES_USER")
    db_name: str = Field(alias="POSTGRES_DB")
    secret_key: str = Field(alias="SECRET_KEY")
    algorithm: str = Field(alias="ALGORITHM")
    access_exp: int = Field(alias="access_token_expire_minutes")
    refresh_exp: int = Field(alias="refresh_token_expire_days")
    redis_host: str = Field(alias="REDIS_HOST")
    redis_port: int = Field(alias="REDIS_PORT")
    test_db_name: str = Field(alias="TEST_POSTGRES_DB")
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_psw}@postgres:5432/{self.db_name}"

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/0"

    @property
    def test_redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/1"

    @property
    def test_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_psw}@postgres_test:5432/{self.test_db_name}"


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
