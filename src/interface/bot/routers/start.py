from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, URLInputFile, WebAppInfo

from src.application import commands
from src.application.commands import CreateUserCommand
from src.application.di.container import StoreContainer
from src.domain.models import ItemFeatures, UserFeatures
from src.infrastructure.repositories import RedisRepository
from src.interface.bot.messages import Messages
from src.settings import TELEGRAM

start_router = Router()


def get_start_keyboard() -> InlineKeyboardMarkup:
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

    keyboard = get_start_keyboard()

    await message.answer(Messages.start_message, reply_markup=keyboard, disable_web_page_preview=True)


def get_recommendation_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text="Посмотреть другие", web_app=WebAppInfo(url=f"{TELEGRAM.url}{TELEGRAM.search_page}")
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@start_router.message(F.text)
async def handle_all_messages(message: Message, container: StoreContainer) -> None:
    stage_meta = commands.PersonalMetaCommand(user_id=message.from_user.id)
    user_feature = UserFeatures(user_id=message.from_user.id, last_search_message=message.text)
    cache_repo: RedisRepository = await container.redis_repository()
    await cache_repo.save_user_features(user_feature)
    pipeline = await container.get_search_recommendation_pipeline(stage_meta=stage_meta)
    collection = await pipeline.execute()
    item: ItemFeatures = collection.items[0]
    message_text = f"*{item.name}* \n\n {item.description}"
    await message.answer_photo(photo=URLInputFile(item.poster.url))
    await message.answer(message_text, reply_markup=get_recommendation_keyboard(), disable_web_page_preview=True)
