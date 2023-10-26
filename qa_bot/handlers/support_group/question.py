from aiogram import html, types
from aiogram.fsm.context import FSMContext

from qa_bot.data import config
from qa_bot.keyboards.inline.reactions import make_reaction_keyboard
from qa_bot.web_handlers import api


async def new_msg_in_group(msg: types.Message) -> None:
    if msg.from_user is None:
        return

    question_text = msg.text
    question_msg_id = msg.message_id
    admin_chat_id = config.ADMIN_CHAT_ID
    username_url = f'<a href="tg://user?id={msg.from_user.id}">{html.quote(msg.from_user.full_name)}</a>'

    result = api.send_message_to_api(question_text)
    if result == 1:
        answer_text = "Ответ"
        rkb = make_reaction_keyboard(admin_chat_id=admin_chat_id,
                                     q_msg_id=question_msg_id)

        response_message = [
            'Ответ на Ваш вопрос:',
            f'<code>{answer_text}</code>',
            '\nПомог ли вам ответ?',
            '👍 – Да',
            '👎 – Нет',
        ]

        await msg.reply(text='\n'.join(response_message),
                        reply_markup=rkb)

    elif result == 2:
        user_question_message = [
            f'Пользователь {username_url} задал вопрос, ответ на который не нашелся в системе:',
            f'<code>{html.quote(msg.text)}</code>',
            '\nЧтобы ответить на вопрос введите:',
            f'<code>/ответить {msg.chat.id} {msg.message_id} Ваш_ответ</code>',
        ]
        await msg.reply('Подождите немного, админ ответит на этот вопрос через некоторое время.')
        await msg.bot.send_message(chat_id=admin_chat_id, text="\n".join(user_question_message))


async def last_question(msg: types.Message, state: FSMContext):
    admin_chat_id = config.ADMIN_CHAT_ID
    username_url = f'<a href="tg://user?id={msg.from_user.id}">{html.quote(msg.from_user.full_name)}</a>'
    user_question_message = [
        f'Пользователю {username_url} не понравился ответ. Он задал еще один вопрос:',
        f'<code>{html.quote(msg.text)}</code>',
        '\nЧтобы ответить на вопрос введите:',
        f'<code>/ответить {msg.chat.id} {msg.message_id} Ваш_ответ</code>',
    ]
    await msg.reply('Подождите немного, админ ответит на этот вопрос через некоторое время.')
    await msg.bot.send_message(chat_id=admin_chat_id, text="\n".join(user_question_message))
    await state.clear()
