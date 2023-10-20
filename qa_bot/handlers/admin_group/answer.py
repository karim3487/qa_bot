from aiogram import types


async def answer_the_question(msg: types.Message) -> None:
    if msg.from_user is None:
        return
    await msg.answer("Is admin chat")
