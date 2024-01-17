from typing import Optional

from aiogram.filters.callback_data import CallbackData


class StartAnsweringCallback(CallbackData, prefix="start_a"):
    q_msg_id: int
    answers_id: Optional[str] = None


class CancelAnsweringCallback(CallbackData, prefix="cancel_a"):
    answering_id: int
    q_msg_id: int


class ReactionCallback(CallbackData, prefix="reaction"):
    # Whether the answer was helpful
    is_help: bool
    # Chat ID with administrators
    admin_chat_id: str
    # Message ID with the administrator's response
    answer_msg_id: Optional[int] = None
    # Message ID of the question
    question_msg_id: Optional[int] = None


class PagesCallback(CallbackData, prefix="pages"):
    page: Optional[int] = 1
    stop: Optional[bool] = False


class AnswerCallback(CallbackData, prefix="answer"):
    answer_id: int
