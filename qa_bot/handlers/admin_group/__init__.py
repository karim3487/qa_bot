from aiogram import F, Router
from aiogram.filters import Command

from qa_bot.filters import ChatTypeFilter, IsAdminChat

from ...keyboards.inline.callbacks import AnswerCallback
from ...states.admin_chat import AdminChatAnswerStates
from . import answer, callbacks, add_answer


def prepare_router() -> Router:
    admin_group_router = Router()
    admin_group_router.message.filter(
        ChatTypeFilter("supergroup"),
        IsAdminChat(),
        # F.text,
    )

    admin_group_router.message.register(
        add_answer.add_new_answer,
        Command("add_answer"),
    )

    admin_group_router.callback_query.register(
        callbacks.write_answer_callback,
        AnswerCallback.filter(),

    )

    admin_group_router.message.register(
        answer.answer_the_question,
        AdminChatAnswerStates.write_answer
    )

    return admin_group_router
