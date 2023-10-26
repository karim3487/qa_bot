from typing import Optional

from aiogram.filters.callback_data import CallbackData


class AnswerCallback(CallbackData, prefix="answer"):
    # Message ID of the question
    question_msg_id: int
    # Chat ID with support where the question originated
    support_chat_id: int
    # ID of the person who asked the question
    asker_id: int


class ReactionCallback(CallbackData, prefix="reaction"):
    # Whether the answer was helpful
    is_help: bool
    # Chat ID with administrators
    admin_chat_id: str
    # Message ID with the administrator's response
    answer_msg_id: Optional[int] = None
    # Message ID of the question
    question_msg_id: Optional[int] = None
