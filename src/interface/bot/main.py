from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from src.interface.bot.routers.start import start_router
from src.interface.settings import TgConfig


async def main():
    bot = Bot(TgConfig().token)
    dp = Dispatcher()
    dp.include_routers(
        start_router,
    )
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
