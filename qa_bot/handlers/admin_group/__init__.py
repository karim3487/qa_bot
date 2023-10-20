from aiogram import Router

from qa_bot.filters import ChatTypeFilter, IsAdminChat

from . import answer


def prepare_router() -> Router:
    group_router = Router()
    group_router.message.filter(ChatTypeFilter("supergroup"))

    group_router.message.register(
        answer.answer_the_question,
        IsAdminChat(),
    )

    return group_router
