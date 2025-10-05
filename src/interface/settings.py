from pydantic import Field
from pydantic_settings import BaseSettings


class TgConfig(BaseSettings):
    token: str = Field(alias="TG_BOT_TOKEN")
    url: str = Field(default="one-more-episode.ru/", alias="TG_WEB_APP_URL")
    onboarding_page: str = "/onboarding"


TG_CONF = TgConfig()
