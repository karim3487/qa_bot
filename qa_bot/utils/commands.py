from aiogram import types, Bot

from qa_bot.data import config


async def set_default_commands(bot: Bot):
    default_commands = [
        types.BotCommand(command="start", description="Запуск бота"),
        types.BotCommand(command="help", description="Помощь"),
    ]
    await bot.set_my_commands(
        default_commands,
        scope=types.BotCommandScopeAllPrivateChats()
    )

    admin_chat_commands = [
        types.BotCommand(command="add_answer", description="Добавить ответ"),
        types.BotCommand(command="get_chat_id", description="Получить ID чата"),
    ]
    await bot.set_my_commands(
        admin_chat_commands,
        scope=types.BotCommandScopeChat(chat_id=config.ADMIN_CHAT_ID),
    )
