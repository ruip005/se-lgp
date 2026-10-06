"""Configuração lida do ficheiro .env (prefixo LGP_). Nada fixo no código."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="LGP_", extra="ignore")

    camera_index: int = 0
    camera_width: int = 640
    camera_height: int = 480
    model_path: str = "models/hand_landmarker.task"
    serial_port: str | None = None
    serial_baud: int = 115200


@lru_cache
def get_settings() -> Settings:
    return Settings()
