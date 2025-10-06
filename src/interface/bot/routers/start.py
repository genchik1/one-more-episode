from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, WebAppInfo

from src.application.commands import CreateUserCommand
from src.application.di.container import StoreContainer
from src.interface.bot.messages import Messages
from src.settings import TELEGRAM

start_router = Router()


def get_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text="Пройти онбординг", web_app=WebAppInfo(url=f"{TELEGRAM.url}{TELEGRAM.onboarding_page}")
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@start_router.message(CommandStart(deep_link=True))
@start_router.message(Command("start"))  # TODO возможно вынести эти команды
async def start_command(message: Message, container: StoreContainer) -> None:
    user_command = CreateUserCommand(user_id=message.from_user.id, username=message.from_user.username)
    create_user_use_case = await container.create_user_use_case()
    await create_user_use_case.execute(user_command)

    keyboard = get_keyboard()

    await message.answer(Messages.start_message, reply_markup=keyboard, disable_web_page_preview=True)
