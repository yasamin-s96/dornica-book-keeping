from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import MySQLDsn, Field, validator, field_validator
from dotenv import load_dotenv


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8",
    )
    app_host: str
    app_port: str
    secret_key: str
    mysql_dsn: MySQLDsn
    secret_key: str
    jwt_algorithm: str = Field(alias="algorithm")
    jwt_expire_time: int = Field(alias="expire_after_days")
    whitelist_token_expire_time: int = Field(
        alias="redis_whitelist_token_expire_after_seconds"
    )
    email_token_expire_time: int = Field(alias="expire_after_minutes")
    email_host: str
    email_host_user: str
    email_host_password: str
    email_port: int
    email_use_tls: bool

    image_host: str
    image_port: int
    image_max_size_in_mb: int = 5
    image_max_size_in_bytes: int = 5 * 1024 * 1024
    image_extensions: list[str] = Field(default=["jpg", "jpeg", "png"])
    image_content_types: list[str] = Field(default=["image/jpeg", "image/png"])
    origins: list[str] = ["*"]


settings = Settings()
