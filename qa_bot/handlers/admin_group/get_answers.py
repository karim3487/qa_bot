from aiogram import types, html

from qa_bot.keyboards.inline.callbacks import PagesCallback
from qa_bot.keyboards.inline.pages import make_pages_keyboard
from qa_bot.utils.api.answer_list import AnswerList
from qa_bot.utils.api.auto_responder_api import auto_responder_api


async def create_pagination_message(answer_list: AnswerList):
    answers = [
        f"{answer_list.offset + i + 1}. {html.code(html.quote(answer.text))}"
        for i, answer in enumerate(answer_list.answers)
    ]
    message_content = [
        f"{html.bold(f'Ответы {answer_list.offset + 1}-{answer_list.offset + len(answer_list.answers)} из {answer_list.count_answers}')}\n",
        *answers,
    ]
    keyboard = make_pages_keyboard(
        current_page=answer_list.current_page, total_pages=answer_list.total_pages
    )
    return "\n".join(message_content), keyboard


async def get_answers(msg: types.Message):
    data = await auto_responder_api.get_answers()
    answer_list = AnswerList(data)
    message_content, keyboard = await create_pagination_message(answer_list)
    await msg.answer(message_content, reply_markup=keyboard)


async def pagination(callback_query: types.CallbackQuery, callback_data: PagesCallback):
    answer_list = AnswerList({})

    if callback_data.stop:
        await callback_query.answer("Вы не можете переключиться на эту страницу")
        return

    await answer_list.go_to_page(callback_data.page)
    message_content, keyboard = await create_pagination_message(answer_list)
    await callback_query.message.edit_text(message_content, reply_markup=keyboard)
