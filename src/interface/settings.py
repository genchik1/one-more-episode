from pydantic import Field
from pydantic_settings import BaseSettings


class TgConfig(BaseSettings):
    token: str = Field(alias="TG_BOT_TOKEN")
    url: str = "localhost"
    onboarding_page: str = url + "/onboarding"


TG_CONF = TgConfig()
