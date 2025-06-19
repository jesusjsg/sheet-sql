from typing import Annotated, Any, List, Literal
from pydantic import AnyUrl, computed_field
from pydantic.functional_validators import BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> List[str]:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list):
        return v
    else:
        raise ValueError("cors must be a string or list")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        env_prefix="APP_",
        extra="ignore",
    )

    # FastAPI settings
    APP_TITLE: str = "Sheet SQL"
    APP_DESCRIPTION: str = "A simple SQL sheet"
    APP_VERSION: str = "0.1.0"
    APP_DEBUG: bool = False
    APP_ENVIRONMENT: Literal["development", "testing", "production"] = (
        "development"
    )

    # CORS settings
    APP_BACKEND_CORS_ORIGINS: Annotated[
        List[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []
    APP_FRONTEND_HOST: str = "http://localhost"

    @computed_field
    @property
    def all_cors_origins(self) -> List[str]:
        return [
            str(origin).rstrip("/") for origin in self.APP_BACKEND_CORS_ORIGINS
        ] + [self.APP_FRONTEND_HOST]


settings = Settings()
