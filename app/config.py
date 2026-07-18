from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./ecommerce.db"
    secret_key: str = "change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    redis_url: str = "redis://localhost:6379/0"
    product_cache_ttl: int = 60
    rate_limit_times: int = 5
    rate_limit_seconds: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
