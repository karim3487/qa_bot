from aiogram import types, html

from qa_bot.utils.api.auto_responder_api import auto_responder_api


async def get_answers(msg: types.Message):
    answers = await auto_responder_api.get_list_of_answers()
    m = []
    for i, answer in enumerate(answers):
        m.append(f"{i + 1}. {html.code(html.quote(answer))}\n")

    await msg.reply("\n".join(m))
