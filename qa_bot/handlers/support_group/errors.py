from aiogram import Bot
from aiogram.types import ErrorEvent

from qa_bot.utils.messages import MESSAGES
from qa_bot.data import config


async def it_is_not_question(event: ErrorEvent):
    pass


async def handle_other_errors(event: ErrorEvent, bot: Bot):
    msg = event.update.message
    cid = msg.chat.id
    await msg.answer(MESSAGES.Errors.other)

    m = MESSAGES.Errors.report_message(cid, event.exception)
    await bot.send_message(config.DEV_ID, m)
