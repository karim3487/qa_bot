import re

from aiogram import types

from qa_bot.utils.api.auto_responder_api import auto_responder_api
from qa_bot.utils.messages import MESSAGES


async def add_new_answer(msg: types.Message):
    if not msg.reply_to_message:
        await msg.answer(MESSAGES.Errors.add_answer)
        return

    regex_pattern = r"/ответить -\d+ \d+ .+"
    answer = msg.reply_to_message.text

    if re.match(regex_pattern, answer):
        answer = answer.split(" ", 3)[-1]

    await auto_responder_api.add_answer(answer)

    await msg.reply(MESSAGES.Info.add_answer(answer))
