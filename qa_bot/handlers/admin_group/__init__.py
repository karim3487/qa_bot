from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, ExceptionTypeFilter

from qa_bot.filters import ChatTypeFilter, IsAdminChat

from ...keyboards.inline.callbacks import (
    CancelAnsweringCallback,
    StartAnsweringCallback,
)
from . import add_answer, answer, callbacks, errors, get_answers
from ...utils.exceptions import AnswerAlreadyExists


def prepare_router() -> Router:
    admin_group_router = Router()
    admin_group_router.message.filter(
        ChatTypeFilter("supergroup"),
        IsAdminChat(),
        F.text,
    )

    admin_group_router.message.register(
        get_answers.get_answers,
        Command("get_answers"),
    )

    admin_group_router.message.register(
        add_answer.add_new_answer,
        Command("add_answer"),
    )

    admin_group_router.message.register(
        answer.answer_the_question,
        Command("ответить"),
    )

    admin_group_router.callback_query.register(
        callbacks.start_answering_callback,
        StartAnsweringCallback.filter(),
    )

    admin_group_router.callback_query.register(
        callbacks.cancel_answering_callback,
        CancelAnsweringCallback.filter(),
    )

    admin_group_router.error.register(
        errors.answer_already_exists,
        ExceptionTypeFilter(AnswerAlreadyExists),
    )

    admin_group_router.error.register(
        errors.handle_not_found_cid_and_mid,
        ExceptionTypeFilter(TelegramBadRequest),
    )

    # admin_group_router.error.register(
    #     errors.handle_other_errors,
    # )

    return admin_group_router
