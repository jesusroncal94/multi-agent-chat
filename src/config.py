from datetime import timedelta

from pydantic import AnyHttpUrl, BaseModel, Field, SecretStr, field_serializer
from pydantic_settings import BaseSettings, SettingsConfigDict


class OAIConfig(BaseModel):
    model: str = Field(alias="model")
    api_type: str = Field(alias="api_type")
    api_key: SecretStr = Field(alias="api_key")
    base_url: AnyHttpUrl = Field(alias="base_url")
    api_version: str = Field(alias="api_version")

    @field_serializer("api_key", when_used="always")
    def dump_api_key(self, value: SecretStr):
        return value.get_secret_value()

    @field_serializer("base_url", when_used="always")
    def dump_base_url(self, value: AnyHttpUrl):
        return str(value)


class Settings(BaseSettings):
    redis_host: str = Field(alias="REDIS_HOST")
    redis_port: int = Field(alias="REDIS_PORT")
    redis_db: int = Field(alias="REDIS_DB")
    chat_session_ttl: timedelta = Field(
        default=timedelta(hours=24), alias="CHAT_SESSION_TTL"
    )
    oai_config_list: list[OAIConfig] = Field(
        default=timedelta(hours=24), alias="OAI_CONFIG_LIST"
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
