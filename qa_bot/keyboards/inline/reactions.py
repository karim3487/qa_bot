from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callbacks import ReactionCallback


def make_reaction_keyboard(admin_chat_id: int, answer_msg_id: int, answer_msg_text: str,
                           asker_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    actions = [
        {
            'text': '👍',
            'callback_data': ReactionCallback(is_help=True, admin_chat_id=admin_chat_id, answer_msg_id=answer_msg_id,
                                              answer_msg_text=answer_msg_text, asker_id=asker_id),
        },
        {
            'text': '👎',
            'callback_data': ReactionCallback(is_help=False, admin_chat_id=admin_chat_id, answer_msg_id=answer_msg_id,
                                              answer_msg_text=answer_msg_text, asker_id=asker_id),
        },
    ]

    for action in actions:
        builder.button(text=action['text'], callback_data=action['callback_data'])

    builder.adjust(2)
    return builder.as_markup()
