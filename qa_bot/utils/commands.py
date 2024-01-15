from aiogram import types, Bot
from aiogram.exceptions import TelegramBadRequest

from qa_bot.data import config


async def set_default_commands(bot: Bot) -> None:
    default_commands = [
        types.BotCommand(command="start", description="Запуск бота"),
        types.BotCommand(command="help", description="Помощь"),
    ]
    await bot.set_my_commands(
        default_commands,
        scope=types.BotCommandScopeAllPrivateChats()
    )
    try:
        admin_chat_commands = [
            types.BotCommand(command="add_answer", description="Добавить ответ"),
            types.BotCommand(command="get_answers", description="Вывести все ответы из БД"),
            types.BotCommand(command="get_chat_id", description="Получить ID чата"),
        ]
        await bot.set_my_commands(
            admin_chat_commands,
            scope=types.BotCommandScopeChat(chat_id=config.ADMIN_CHAT_ID),
        )
    except TelegramBadRequest as e:
        if 'chat not found' in str(e):
            pass
