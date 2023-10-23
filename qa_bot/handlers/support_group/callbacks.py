from aiogram import types, Bot
from qa_bot.keyboards.inline.callbacks import ReactionCallback

async def reaction_on_answer_callback(callback_query: types.CallbackQuery, callback_data: ReactionCallback, bot: Bot) -> None:
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id

    if callback_data.asker_id != user_id:
        await callback_query.answer('Простите, это не Вы задавали этот вопрос')
    elif not callback_data.answer_msg_id:
        user_response = [
            'Ответ на Ваш вопрос:',
            f'<code>{callback_data.answer_msg_text}</code>',
            '\nСпасибо за отзыв'
        ]
        await bot.edit_message_text('\n'.join(user_response), chat_id=chat_id, message_id=message_id)

        admin_notification = [
            'Вопрос:',
            f'<code>{callback_data.question_text}</code>',
            '\nОтвет системы:',
            f'<code>{callback_data.answer_msg_text}</code>',
            '\nПользователю не помог ответ от системы'
        ]
        await bot.send_message(chat_id=callback_data.admin_chat_id, text='\n'.join(admin_notification))
        await callback_query.answer()
    else:
        if callback_data.is_help:
            admin_response = [
                'Ответ от администратора:',
                callback_data.answer_msg_text,
                '\nСпасибо за отзыв'
            ]
            await bot.edit_message_text('\n'.join(admin_response), chat_id=chat_id, message_id=message_id)
        else:
            await bot.send_message(callback_data.admin_chat_id, text='Ваш ответ не помог пользователю', reply_to_message_id=callback_data.answer_msg_id)
            admin_response = [
                'Ответ от администратора:',
                callback_data.answer_msg_text,
                '\nСпасибо за отзыв'
            ]
            await bot.edit_message_text('\n'.join(admin_response), chat_id=chat_id, message_id=message_id)

        await callback_query.answer()
