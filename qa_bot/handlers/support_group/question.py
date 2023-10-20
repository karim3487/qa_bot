from aiogram import html, types

from qa_bot.data import config
from qa_bot.web_handlers import api


async def new_mgs_in_group(msg: types.Message) -> None:
    if msg.from_user is None:
        return
    result = await api.send_message_to_api(msg.text)

    admin_chat_id = config.ADMIN_CHAT_ID
    username_url = f'<a href="tg://user?id={msg.from_user.id}">{html.quote(msg.from_user.full_name)}</a>'
    if result == 2:
        m = [
            f'Пользователь {username_url} задал вопрос, ответ на который не нашелся в системе:',
            f'{msg.text}\n',
        ]
        await msg.bot.send_message(chat_id=admin_chat_id, text="\n".join(m))
