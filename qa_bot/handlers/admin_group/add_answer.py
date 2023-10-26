import re

from aiogram import types

from qa_bot.web_handlers import api


async def add_new_answer(msg: types.Message):
    if not msg.reply_to_message:
        await msg.answer('Вы должны ответить на какое-нибудь сообщение этой командой, чтобы добавить ответ в БД.')
        return

    regex_pattern = r'/ответить -\d+ \d+ .+'
    answer = msg.reply_to_message.text

    if re.match(regex_pattern, answer):
        answer = answer.split(' ', 3)[-1]

    res = api.add_answer(answer)
    # if res.status_code == 200:
    if res['status_code'] == 200:
        m = [
            'Ответ добавлен в БД:',
            f'<code>{answer}</code>',
        ]

        await msg.reply('\n'.join(m))
