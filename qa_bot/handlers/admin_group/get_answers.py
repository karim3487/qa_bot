from aiogram import types, html

from qa_bot.keyboards.inline.callbacks import PagesCallback
from qa_bot.keyboards.inline.pages import make_pages_keyboard
from qa_bot.utils.api.answer import Answer
from qa_bot.utils.api.auto_responder_api import auto_responder_api
from qa_bot.utils.messages import MESSAGES


def calculate_total_pages(total_answers: int, answers_per_page: int) -> int:
    total_pages = total_answers // answers_per_page
    if total_answers % answers_per_page > 0:
        total_pages += 1
    return total_pages


def calculate_answer_num(page: int, answers_per_page: int, index: int) -> int:
    return (page - 1) * answers_per_page + index + 1


def calculate_offset(page: int, answers_per_page: int) -> int:
    return page * answers_per_page - answers_per_page


async def create_pagination_message(
    page: int, answers: list[Answer], total_answers: int
) -> tuple[str, types.InlineKeyboardMarkup]:
    answers_per_page = auto_responder_api.answers_per_page
    offset = (page - 1) * len(answers)
    total_pages = calculate_total_pages(total_answers, answers_per_page)

    answers = [
        f"\n#️⃣{calculate_answer_num(page, answers_per_page, i)}. {html.code(html.quote(answer.text))}"
        for i, answer in enumerate(answers)
    ]
    message_content = [
        f"{html.bold(f'Ответы {offset + 1}-{offset + len(answers)} из {total_answers}')}\n",
        *answers,
    ]
    keyboard = make_pages_keyboard(current_page=page, total_pages=total_pages)
    return "\n".join(message_content), keyboard


async def get_answers(msg: types.Message) -> None:
    data = await auto_responder_api.get_answers()
    answer_list = [Answer.from_dict(answer) for answer in data["results"]]
    total_answers = data["count"]
    message_content, keyboard = await create_pagination_message(
        1, answer_list, total_answers
    )
    await msg.answer(message_content, reply_markup=keyboard)


async def pagination(
    callback_query: types.CallbackQuery, callback_data: PagesCallback
) -> None:
    if callback_data.stop:
        await callback_query.answer(MESSAGES.Errors.cannot_change_page)
        return
    page = callback_data.page

    answers_per_page = auto_responder_api.answers_per_page
    offset = calculate_offset(page, answers_per_page)
    data = await auto_responder_api.get_answers(offset)
    answer_list = [Answer.from_dict(answer) for answer in data["results"]]
    total_answers = data["count"]
    message_content, keyboard = await create_pagination_message(
        page, answer_list, total_answers
    )

    await callback_query.message.edit_text(message_content, reply_markup=keyboard)
