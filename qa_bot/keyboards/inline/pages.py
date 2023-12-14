from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from qa_bot.keyboards.inline.callbacks import PagesCallback


def make_pages_keyboard(current_page: int, total_pages: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    prev_text = "◀️"
    prev_callback_data = PagesCallback(page=current_page - 1)
    if current_page == 1:
        prev_text = "🛑"
        prev_callback_data = PagesCallback(stop=True)

    next_text = "▶️"
    next_callback_data = PagesCallback(page=current_page + 1)
    if current_page == total_pages:
        next_text = "🛑"
        next_callback_data = PagesCallback(stop=True)

    actions = [
        {"text": prev_text, "callback_data": prev_callback_data},
        {
            "text": f"{current_page}/{total_pages}",
            "callback_data": PagesCallback(),
        },
        {"text": next_text, "callback_data": next_callback_data},
    ]

    for action in actions:
        builder.button(
            text=action.get("text"), callback_data=action.get("callback_data")
        )

    builder.adjust(3)
    return builder.as_markup()
