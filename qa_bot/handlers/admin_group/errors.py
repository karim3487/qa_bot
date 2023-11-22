from aiogram import Bot, html
from aiogram.types import ErrorEvent

from qa_bot.data import config


async def handle_not_found_cid_and_mid(event: ErrorEvent):
    m = [
        "Не получается найти чат с таким ID или сообщение!",
        "Попробуйте еще раз",
    ]
    await event.update.message.answer("\n".join(m))


async def handle_other_errors(event: ErrorEvent, bot: Bot):
    msg = event.update.message
    cid = msg.chat.id
    m = [
        f'Упс! {html.bold("Ошибка!")} Не переживайте, ошибка уже {html.bold("отправлена")} разработчику.',
    ]
    await msg.answer("\n".join(m))

    m = [
        f'Случилась {html.bold("ошибка")} в чате {html.bold(cid)}',
        f"Статус ошибки: {html.code(event.exception)}",
    ]
    await bot.send_message(config.DEV_ID, "\n".join(m))
