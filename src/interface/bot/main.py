from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware, Bot, Dispatcher
from aiogram.types import Message

from src.application.di.container import StoreContainer
from src.interface.bot.routers.start import start_router
from src.settings import TgConfig


class DIMiddleware(BaseMiddleware):
    def __init__(self, container: StoreContainer):
        self.container = container
        super().__init__()

    async def __call__(
        self, handler: Callable[[Message, dict[str, Any]], Awaitable[Any]], event: Message, data: dict[str, Any]
    ) -> Any:
        data["container"] = self.container
        return await handler(event, data)


async def main() -> None:
    container = StoreContainer()
    bot = Bot(TgConfig().token)
    dp = Dispatcher()
    dp.message.middleware(DIMiddleware(container))
    dp.include_routers(
        start_router,
    )
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
