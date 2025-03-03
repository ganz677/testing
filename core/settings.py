from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = 'sqlite+aiosqlite:///./db.sqlite3'
    db_echo: bool = True
    api_v1_prefix: str = '/api/v1'



settings = Settings()