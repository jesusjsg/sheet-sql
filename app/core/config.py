from typing import Annotated, Any, Literal
from pydantic import AnyUrl, BeforeValidator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        env_prefix="APP_",
        extra="ignore",
    )
    APP_API_V1_STR: str = "/api/v1"
    APP_PROJECT_NAME: str = "sheet-sql"
    APP_DEBUG: bool = True
    APP_ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    APP_BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []
    APP_FRONTEND_HOST: str = "http://localhost:5173"

    @computed_field
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.APP_BACKEND_CORS_ORIGINS] + [
            self.APP_FRONTEND_HOST
        ]


settings = Settings()

print(settings.model_dump())
