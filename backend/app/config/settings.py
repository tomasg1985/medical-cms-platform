"""
Configuración principal de la aplicación.

Los valores se obtienen desde variables de entorno
y/o desde el archivo .env.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuración de Medical CMS Platform.
    """

    app_name: str = "Medical CMS Platform API"
    app_version: str = "0.1.0"
    debug: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()