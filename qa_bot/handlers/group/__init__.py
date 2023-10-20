from aiogram import Router
from aiogram.filters import CommandStart, StateFilter

from qa_bot import states
from qa_bot.filters import ChatTypeFilter, TextFilter

from . import echo


def prepare_router() -> Router:
    group_router = Router()
    group_router.message.filter(ChatTypeFilter("supergroup"))

    group_router.message.register(
        echo.echo
    )

    return group_router
