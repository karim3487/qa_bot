from aiogram import Router

from qa_bot.filters import ChatTypeFilter, IsSupportChat

from . import echo, question


def prepare_router() -> Router:
    group_router = Router()
    group_router.message.filter(ChatTypeFilter("supergroup"))

    group_router.message.register(
        question.new_mgs_in_group,
        IsSupportChat(),
    )
    group_router.message.register(
        echo.echo
    )

    return group_router
