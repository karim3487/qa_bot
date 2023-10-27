
from aiogram import Bot, types
from aiogram.fsm.context import FSMContext

from qa_bot.keyboards.inline.answer import (
    make_cancel_answer_keyboard,
    make_start_answer_keyboard,
)
from qa_bot.keyboards.inline.callbacks import (
    CancelAnsweringCallback,
    StartAnsweringCallback,
)


async def start_answering_callback(callback_query: types.CallbackQuery, callback_data: StartAnsweringCallback,
                                   bot: Bot, state: FSMContext) -> None:
    await state.update_data(msg_html=callback_query.message.html_text)
    username = callback_query.from_user.username

    if username:
        username = f'@{username}'
    else:
        username = callback_query.from_user.full_name

    m = [
        callback_query.message.html_text,
        '\nЧтобы ответить на вопрос введите:',
        f'<code>/ответить {callback_data.support_chat_id} {callback_data.q_msg_id} Ваш_ответ</code>',
        f'\nЗа ответ взялся {username}'
    ]

    rkb = make_cancel_answer_keyboard(answering_id=callback_query.from_user.id,
                                      support_chat_id=callback_data.support_chat_id,
                                      q_msg_id=callback_data.q_msg_id)

    await bot.edit_message_text('\n'.join(m), callback_query.message.chat.id, callback_query.message.message_id,
                                reply_markup=rkb)

    answering = callback_query.from_user.username
    print(answering)
    await callback_query.answer()


async def cancel_answering_callback(callback_query: types.CallbackQuery, callback_data: CancelAnsweringCallback,
                                    bot: Bot, state: FSMContext) -> None:
    if callback_query.from_user.id != callback_data.answering_id:
        await callback_query.answer("На этот вопрос отвечает другой администратор.")
        return
    data = await state.get_data()
    m = [
        data['msg_html'],
    ]

    rkb = make_start_answer_keyboard(support_chat_id=callback_data.support_chat_id, q_msg_id=callback_data.q_msg_id)

    await bot.edit_message_text('\n'.join(m), callback_query.message.chat.id,
                                callback_query.message.message_id,
                                reply_markup=rkb)

    await callback_query.answer()
