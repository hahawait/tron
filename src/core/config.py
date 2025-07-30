from dataclasses import dataclass
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

Mode = Literal["LOCAL", "DEV", "PROD"]
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


class AppConfig(BaseConfig):
    mode: Mode = Field(alias="APP_MODE")
    log_level: LogLevel = Field(alias="APP_LOGGING_LEVEL")
    title: str = Field(alias="APP_TITLE")
    description: str = Field(alias="APP_DESCRIPTION")
    version: str = Field(alias="APP_VERSION")
    admin_username: str = Field(alias="APP_ADMIN_USERNAME")
    admin_password: str = Field(alias="APP_ADMIN_PASSWORD")

    @property
    def is_prod(self) -> bool:
        return self.mode == "PROD"

    @property
    def is_dev(self) -> bool:
        return self.mode == "DEV"

    @property
    def is_local(self) -> bool:
        return self.mode == "LOCAL"


class PGConfig(BaseConfig):
    host: str = Field(alias="POSTGRES_HOST")
    port: int = Field(alias="POSTGRES_PORT")
    user: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD")
    db: str = Field(alias="POSTGRES_DB_NAME")

    @property
    def dsn(self) -> str:
        user = f"{self.user}:{self.password}"
        db = f"{self.host}:{self.port}/{self.db}"
        return f"postgresql+asyncpg://{user}@{db}"


class TronConfig(BaseConfig):
    network: str = Field(alias="TRON_NETWORK")


@dataclass
class Config:
    app: AppConfig
    pg: PGConfig
    tron: TronConfig


def get_config() -> Config:
    return Config(
        app=AppConfig(),
        pg=PGConfig(),
        tron=TronConfig(),
    )
