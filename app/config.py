from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    db_psw: str = Field(alias="POSTGRES_PASSWORD")
    db_user: str = Field(alias="POSTGRES_USER")
    db_name: str = Field(alias="POSTGRES_DB")
    db_host: str = Field(default="postgres", alias="POSTGRES_HOST")
    db_port: int = Field(default=5432, alias="POSTGRES_PORT")
    
    test_db_name: str = Field(default="test_db", alias="TEST_POSTGRES_DB")
    test_db_host: str = Field(default="postgres_test", alias="TEST_POSTGRES_HOST")
    test_db_port: int = Field(default=5432, alias="TEST_POSTGRES_PORT")
    
    
    secret_key: str = Field(alias="SECRET_KEY")
    algorithm: str = Field(alias="ALGORITHM")
    access_exp: int = Field(alias="access_token_expire_minutes")
    refresh_exp: int = Field(alias="refresh_token_expire_days")
    
    redis_host: str = Field(alias="REDIS_HOST")
    redis_port: int = Field(alias="REDIS_PORT")
    
    cookie_secure: bool = Field(default=False, alias="COOKIE_SECURE")
    cors_origins: list[str] = Field(default_factory=list, alias="CORS_ORIGINS")

    
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    
    def _pg_url(self,host:str,port:int,db:str,password:str)->str:
        return URL.create(
            "postgresql+asyncpg",
            username=self.db_user,
            password=password,
            host=host,
            port=port,
            database=db
        ).render_as_string(hide_password=False)
    
    @property
    def database_url(self) -> str:
        return self._pg_url(host=self.db_host,port=self.db_port,db=self.db_name,password=self.db_psw)

    @property
    def test_database_url(self) -> str:
        return self._pg_url(host=self.test_db_host,port=self.test_db_port,db=self.test_db_name,password=self.db_psw)
    
    
    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/0"
    
    @property
    def test_redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/1"


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
