from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: str

    SMTP_HOST: str
    SMTP_PORT: str
    SMTP_USER: str
    SMTP_PASS: str

    DSN: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
