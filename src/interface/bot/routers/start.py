from aiogram import Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, WebAppInfo

from src.application.commands import CreateUserCommand
from src.application.di.container import StoreContainer
from src.interface.bot.messages import Messages
from src.interface.settings import TG_CONF

start_router = Router()
container = StoreContainer()
container.init_resources()
container.wire(modules=[__name__])


def get_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="Уже смотрел...", web_app=WebAppInfo(url=TG_CONF.onboarding_page))],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@start_router.message(CommandStart(deep_link=True))
@start_router.message(Command("start"))  # TODO возможно вынести эти команды
async def start_command(message: Message, command: CommandObject) -> None:
    user_command = CreateUserCommand(user_id=message.from_user.id, username=message.from_user.username)

    await container.create_user_use_case(user_command)

    keyboard = get_keyboard()

    await message.answer(
        Messages.start_message, reply_markup=keyboard, parse_mode=TG_CONF.parse_mode, disable_web_page_preview=True
    )
