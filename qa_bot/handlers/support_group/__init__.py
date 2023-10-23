from aiogram import F, Router

from qa_bot.filters import ChatTypeFilter, IsSupportChat

from ...keyboards.inline.callbacks import ReactionCallback
from . import callbacks, question


def prepare_router() -> Router:
    support_group_router = Router()
    support_group_router.message.filter(
        ChatTypeFilter("supergroup"),
        IsSupportChat(),
        F.text,
    )

    support_group_router.callback_query.register(
        callbacks.reaction_on_answer_callback,
        ReactionCallback.filter(),
    )

    support_group_router.message.register(
        question.new_msg_in_group,
    )

    return support_group_router
