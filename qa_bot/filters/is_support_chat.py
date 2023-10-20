from aiogram.filters import BaseFilter
from aiogram.types import Message

from qa_bot.data import config


class IsSupportChat(BaseFilter):
    def __init__(self):
        self.support_chat_id = config.SUPPORT_CHAT_ID

    async def __call__(self, message: Message) -> bool:
        chat_id = str(message.chat.id)
        return chat_id == self.support_chat_id
