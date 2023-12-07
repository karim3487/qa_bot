from aiogram import types

from qa_bot.utils.messages import MESSAGES


async def get_chat_id(msg: types.Message):
    cid = str(msg.chat.id)

    await msg.answer(MESSAGES.Info.get_chat_id(cid))
