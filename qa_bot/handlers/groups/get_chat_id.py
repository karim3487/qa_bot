from aiogram import types

from qa_bot.utils.messages import MESSAGES_RU


async def get_chat_id(msg: types.Message):
    cid = str(msg.chat.id)

    await msg.answer(MESSAGES_RU.Info.get_chat_id(cid))
