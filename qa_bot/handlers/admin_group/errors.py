from aiogram import Bot
from aiogram.types import ErrorEvent

from qa_bot.utils.messages import MESSAGES
from qa_bot.data import config


async def handle_not_found_cid_and_mid(event: ErrorEvent):
    await event.update.message.answer(MESSAGES.Errors.not_found_cid_or_mid)


async def answer_already_exists(event: ErrorEvent):
    await event.update.message.answer(MESSAGES.Errors.answer_already_exists)


async def handle_other_errors(event: ErrorEvent, bot: Bot):
    msg = event.update.message
    cid = msg.chat.id
    await msg.answer(MESSAGES.Errors.other)

    m = MESSAGES.Errors.report_message(cid, event.exception)
    await bot.send_message(config.DEV_ID, m)
