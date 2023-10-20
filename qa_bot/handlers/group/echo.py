from aiogram import types


async def echo(msg: types.Message) -> None:
    if msg.from_user is None:
        return
    await msg.answer(msg.text)
