from aiogram import Router
from aiogram.filters import CommandStart, StateFilter

from qa_bot import states
from qa_bot.filters import ChatTypeFilter, TextFilter

from . import echo, start


def prepare_router() -> Router:
    user_router = Router()
    user_router.message.filter(ChatTypeFilter("private"))

    user_router.message.register(start.start, CommandStart())
    user_router.message.register(
        start.start,
        TextFilter("🏠В главное меню"),
        StateFilter(states.user.UserMainMenu.menu),
    )
    user_router.message.register(echo.echo)

    return user_router
