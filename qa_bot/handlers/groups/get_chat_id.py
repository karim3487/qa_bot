from aiogram import types, html


async def get_chat_id(msg: types.Message):
    cid = str(msg.chat.id)
    m = [f"ID чата: {html.bold(html.quote(cid))}"]

    await msg.answer("\n".join(m))
