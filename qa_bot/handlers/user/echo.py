from aiogram import html, types
from aiogram.fsm.context import FSMContext

from qa_bot import states


async def echo(msg: types.Message) -> None:
    if msg.from_user is None:
        return
    await msg.answer(msg.text)