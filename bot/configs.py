from typing import Optional

from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    API_TOKEN: str = Field(..., env="TG_API_TOKEN")
    VK_API_TOKEN: str = Field("", env="VK_API_TOKEN")
    VK_API_APP: str = Field("", env="VK_API_APP")


class DatabaseConnectSettings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_USER: str = Field(..., env="MYSQL_USER")
    DB_PASSWORD: str = Field(..., env="MYSQL_ROOT_PASSWORD")
    DB_PORT: int = Field(3306, env="LOCAL_PORT_DB")


class DatabaseNameDBSettings(BaseSettings):
    DB_CDEK_NAME: Optional[str] = None
    DB_MAILRU_NAME: Optional[str] = None
    DB_SUSHI_NAME: Optional[str] = None
    DB_WILDBERRIES_NAME: Optional[str] = None
    DB_YANDEX_NAME: Optional[str] = None
    DB_GIBDD_NAME: Optional[str] = None
    DB_DELIVERY_NAME: Optional[str] = None
    DB_DELIVERY2_NAME: Optional[str] = None
    DB_VTB_NAME: Optional[str] = None
    DB_PIKABU_NAME: Optional[str] = None
    DB_RFCONT_NAME: Optional[str] = None
    DB_OKRUG_NAME: Optional[str] = None
    DB_LINKEDIN_NAME: Optional[str] = None
    DB_BEELINE_NAME: Optional[str] = None


app_settings = AppSettings()
db_connect_settings = DatabaseConnectSettings()
db_name_settings = DatabaseNameDBSettings()
