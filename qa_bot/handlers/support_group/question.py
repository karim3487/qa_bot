from aiogram import html, types

from qa_bot.data import config
from qa_bot.keyboards.inline import answer
from qa_bot.keyboards.inline.reactions import make_reaction_keyboard
from qa_bot.web_handlers import api


async def new_msg_in_group(msg: types.Message) -> None:
    if msg.from_user is None:
        return

    question_text = msg.text
    question_msg_id = msg.message_id
    support_chat_id = msg.chat.id
    admin_chat_id = config.ADMIN_CHAT_ID
    username_url = f'<a href="tg://user?id={msg.from_user.id}">{html.quote(msg.from_user.full_name)}</a>'

    result = api.send_message_to_api(question_text)
    if result == 1:
        answer_text = "Ответ"
        rkb = make_reaction_keyboard(admin_chat_id=int(admin_chat_id),
                                     answer_msg_text=answer_text,
                                     asker_id=msg.from_user.id,
                                     q_text=question_text,
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
            f'<code>{question_text}</code>',
        ]

        await msg.reply('Подождите немного, админ ответит на этот вопрос через некоторое время.')
        rkb = answer.make_answer_keyboard(q=question_text,
                                          q_msg_id=msg.message_id,
                                          support_chat_id=support_chat_id,
                                          asker_id=msg.from_user.id)
        await msg.bot.send_message(chat_id=admin_chat_id, text="\n".join(user_question_message), reply_markup=rkb)
