from pydantic_settings import BaseSettings


class TgConfig(BaseSettings):
    token: str
    url: str = "localhost"
    onboarding_page: str = url + "/onboarding"
    parse_mode = "Markdown"


TG_CONF = TgConfig()
