from typing import List, Optional

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callbacks import AnswerCallback, CancelAnsweringCallback, StartAnsweringCallback


def make_start_answer_keyboard(
    q_msg_id: int, language: str, answers_id: Optional[List[int]] = None
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    actions = [
        {
            "text": "Взяться за ответ",
            "callback_data": StartAnsweringCallback(
                language=language,
                q_msg_id=q_msg_id,
                answers_id=str(answers_id),
            ),
        },
    ]

    for action in actions:
        builder.button(text=action["text"], callback_data=action["callback_data"])

    builder.adjust(1)
    return builder.as_markup()


def make_cancel_answer_keyboard(
    answering_id: int, q_msg_id: int, answers_id: Optional[List[int]] = None
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if answers_id:
        for i, answer_id in enumerate(answers_id):
            builder.button(
                text=f"#️⃣ {i + 1}", callback_data=AnswerCallback(answer_id=answer_id)
            )

    builder.button(
        text="Перестать отвечать",
        callback_data=CancelAnsweringCallback(
            answering_id=answering_id,
            q_msg_id=q_msg_id,
        ),
    )

    builder.adjust(1)
    return builder.as_markup()
