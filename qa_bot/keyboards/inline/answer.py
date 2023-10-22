from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callbacks import AnswerCallback


def make_answer_keyboard(q: str, q_msg_id: int, support_chat_id: int, msg_id_to_edit: int,
                         asker_id: int) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    actions = [
        {
            'text': 'Ответить ✅',
            'callback_data': AnswerCallback(question_text=q,
                                            question_msg_id=q_msg_id,
                                            support_chat_id=support_chat_id,
                                            msg_id_to_edit=msg_id_to_edit,
                                            asker_id=asker_id),
        },
    ]
    for action in actions:
        builder.button(text=action['text'], callback_data=action['callback_data'])

    builder.adjust(1)

    return builder.as_markup()
