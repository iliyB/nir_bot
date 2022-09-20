from typing import Optional

from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    API_TOKEN: str = Field(..., env="TG_API_TOKEN")


class DatabaseSettings(BaseSettings):
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int = 3306

    DB_CDEK_NAME: Optional[str] = None
    DB_MAILRU_NAME: Optional[str] = None
    DB_SUSHI_NAME: Optional[str] = None
    DB_WILDBERIES_NAME: Optional[str] = None
    DB_YANDE_NAME: Optional[str] = None


app_settings = AppSettings()
db_settings = DatabaseSettings()
