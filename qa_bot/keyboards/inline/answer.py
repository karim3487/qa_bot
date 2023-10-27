
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callbacks import CancelAnsweringCallback, StartAnsweringCallback


def make_start_answer_keyboard(support_chat_id: int, q_msg_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    actions = [
        {
            'text': 'Взяться за ответ',
            'callback_data': StartAnsweringCallback(support_chat_id=support_chat_id, q_msg_id=q_msg_id)
        },
    ]

    for action in actions:
        builder.button(text=action['text'], callback_data=action['callback_data'])

    builder.adjust(1)
    return builder.as_markup()


def make_cancel_answer_keyboard(answering_id: int, support_chat_id: int, q_msg_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    actions = [
        {
            'text': 'Перестать отвечать',
            'callback_data': CancelAnsweringCallback(answering_id=answering_id, support_chat_id=support_chat_id,
                                                     q_msg_id=q_msg_id)
        },
    ]

    for action in actions:
        builder.button(text=action['text'], callback_data=action['callback_data'])

    builder.adjust(1)
    return builder.as_markup()
