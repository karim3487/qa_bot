from typing import Optional

from aiogram.filters.callback_data import CallbackData


class AnswerCallback(CallbackData, prefix="answer"):
    # Text of the question
    question_text: str
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
    admin_chat_id: int
    # Message ID with the administrator's response
    answer_msg_id: Optional[int] = None
    # Text of the message with the administrator's response
    answer_msg_text: str
    # ID of the person who asked the question
    asker_id: int
    # Text of the question
    question_text: Optional[str] = None
    # Message ID of the question
    question_msg_id: Optional[int] = None
