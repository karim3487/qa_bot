from aiogram import Router

from qa_bot.filters import ChatTypeFilter, IsAdminChat

from . import answer, echo


def prepare_router() -> Router:
    group_router = Router()
    group_router.message.filter(ChatTypeFilter("supergroup"))

    group_router.message.register(
        answer.answer_the_question,
        IsAdminChat(),
    )
    group_router.message.register(
        echo.echo
    )

    return group_router
