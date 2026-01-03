from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )
    # Actual implementation

    graph_operator_implementation: Optional[str] = None
    cache_implementation: Optional[str] = None
    queue_implementation: Optional[str] = None

    aws_region: Optional[str] = None
    aws_bucket_name: Optional[str] = None
    sqs_queue_url: Optional[str] = None

    redis_password: Optional[str] = None
    redis_host: Optional[str] = None
    redis_port: Optional[str] = None

    neo4j_uri: Optional[str] = None
    neo4j_user: Optional[str] = None
    neo4j_password: Optional[str] = None

    logfire_token: Optional[str] = None
    environment: Optional[str] = None

    gsq_url: Optional[str] = None
    gsq_auth_token: Optional[str] = None

    def __init__(self, **data):
        super().__init__(**data)


@lru_cache
def get_settings() -> Settings:
    return Settings()
