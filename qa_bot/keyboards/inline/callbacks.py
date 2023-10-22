from aiogram.filters.callback_data import CallbackData


class AnswerCallback(CallbackData, prefix="answer"):
    question_text: str
    question_msg_id: int
    support_chat_id: int
    msg_id_to_edit: int
    asker_id: int

class ReactionCallback(CallbackData, prefix="reaction"):
    is_help: bool
    admin_chat_id: int
    answer_msg_id: int
    answer_msg_text: str
    asker_id: int

