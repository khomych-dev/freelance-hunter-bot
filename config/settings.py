from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TELEGRAM_TOKEN: str
    TELEGRAM_CHAT_ID: str
    FREELANCEHUNT_URL: str = "https://freelancehunt.com"
    FREELANCEHUNT_ENDPOINT: str = "/projects?skills%5B0%5D=1&skills%5B1%5D=22&skills%5B2%5D=99"
    PARSE_INTERVAL_SECONDS: int = 300

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
