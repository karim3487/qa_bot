from typing import Optional

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callbacks import ReactionCallback


def make_reaction_keyboard(admin_chat_id: str, answer_msg_id: Optional[int] = None,
                           q_msg_id: Optional[int] = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    actions = [
        {
            'text': '👍',
            'callback_data': ReactionCallback(is_help=True, admin_chat_id=admin_chat_id, answer_msg_id=answer_msg_id,
                                              question_msg_id=q_msg_id),
        },
        {
            'text': '👎',
            'callback_data': ReactionCallback(is_help=False, admin_chat_id=admin_chat_id, answer_msg_id=answer_msg_id,
                                              question_msg_id=q_msg_id),
        },
    ]

    for action in actions:
        builder.button(text=action['text'], callback_data=action['callback_data'])

    builder.adjust(2)
    return builder.as_markup()
