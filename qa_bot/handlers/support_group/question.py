from aiogram import Bot, html, types

from qa_bot.data import config
from qa_bot.keyboards.inline import answer
from qa_bot.keyboards.inline.callbacks import ReactionCallback
from qa_bot.web_handlers import api


async def new_msg_in_group(msg: types.Message) -> None:
    if msg.from_user is None:
        return

    question = msg.text
    support_chat_id = msg.chat.id
    admin_chat_id = config.ADMIN_CHAT_ID
    username_url = f'<a href="tg://user?id={msg.from_user.id}">{html.quote(msg.from_user.full_name)}</a>'

    result = await api.send_message_to_api(question)

    if result == 2:
        user_question_message = [
            f'Пользователь {username_url} задал вопрос, ответ на который не нашелся в системе:',
            f'<code>{question}</code>\n',
        ]

        msg_to_edit = await msg.reply('Подождите немного, админ ответит на этот вопрос через некоторое время.')
        rkb = answer.make_answer_keyboard(q=question,
                                          q_msg_id=msg.message_id,
                                          support_chat_id=support_chat_id,
                                          msg_id_to_edit=msg_to_edit.message_id,
                                          asker_id=msg.from_user.id)
        await msg.bot.send_message(chat_id=admin_chat_id, text="\n".join(user_question_message), reply_markup=rkb)


async def reaction_on_answer_callback(callback_query: types.CallbackQuery, callback_data: ReactionCallback,
                                      bot: Bot) -> None:
    if not callback_data.asker_id == callback_query.from_user.id:
        await callback_query.answer('Простите, это не Вы задавали этот вопрос')
        return

    if callback_data.is_help:
        m = [
            'Ответ от администратора:',
            callback_data.answer_msg_text,
            '\nСпасибо за отзыв'
        ]
        await bot.edit_message_text('\n'.join(m),
                                    chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id)
        await callback_query.answer()
        return

    m = [
        'Ваш ответ не помог пользователю'
    ]

    await bot.send_message(chat_id=callback_data.admin_chat_id, text='\n'.join(m),
                           reply_to_message_id=callback_data.answer_msg_id)
    m = [
        'Ответ от администратора:',
        callback_data.answer_msg_text,
        '\nСпасибо за отзыв'
    ]
    await bot.edit_message_text('\n'.join(m),
                                chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id)
    await callback_query.answer()
