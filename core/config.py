from datetime import timedelta
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Authx Starter"
    app_debag: bool = True

    database_url: str

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expiries_min: int = 15
    refresh_token_expiries_days: int = 7

    model_config = SettingsConfigDict(env_file=".env", env_prefix="", extra="ignore")

    @property
    def access_expiries(self) -> timedelta:
        return timedelta(minutes=self.access_token_expiries_min)

    @property
    def refresh_expiries(self) -> timedelta:
        return timedelta(days=self.refresh_token_expiries_days)

settings =Settings()
