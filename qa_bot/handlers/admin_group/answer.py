from aiogram import Bot, types
from aiogram.fsm.context import FSMContext

from qa_bot.keyboards.inline.callbacks import AnswerCallback
from qa_bot.keyboards.inline.reactions import make_reaction_keyboard
from qa_bot.states.admin_chat import AdminChatAnswerStates


async def write_answer_callback(callback_query: types.CallbackQuery, callback_data: AnswerCallback, bot: Bot,
                                state: FSMContext) -> None:
    admin_chat_id = callback_query.message.chat.id
    msg_to_edit = callback_query.message.message_id
    support_chat_id = callback_data.support_chat_id
    msg_id_to_edit = callback_data.msg_id_to_edit
    question_msg_id = callback_data.question_msg_id
    question_text = callback_data.question_text
    asker_id = callback_data.asker_id

    current_state = await state.get_state()

    if current_state == AdminChatAnswerStates.write_answer:
        await callback_query.answer('Сперва ответьте на вопрос, который Вы взяли в обработку', show_alert=True)
        return

    await state.update_data(support_chat_id=support_chat_id, q_msg_id=question_msg_id, asker_id=asker_id)

    m = [
        f'@{callback_query.from_user.username}, напишите ответ на вопрос и отправьте сообщение:',
        question_text
    ]

    await bot.edit_message_text('\n'.join(m), chat_id=admin_chat_id, message_id=msg_to_edit)

    await state.set_state(AdminChatAnswerStates.write_answer)
    m = [
        'Администратор начал отвечать на Ваш вопрос, подождите...'
    ]

    await bot.edit_message_text('\n'.join(m), chat_id=support_chat_id, message_id=msg_id_to_edit)
    await callback_query.answer()


async def answer_the_question(msg: types.Message, state: FSMContext, bot: Bot) -> None:
    if msg.from_user is None:
        return

    data = await state.get_data()
    admin_chat_id = msg.chat.id
    answer_msg_id = msg.message_id
    answer_msg_text = msg.text
    support_chat_id = data.get('support_chat_id')
    q_msg_id = data.get('q_msg_id')

    if support_chat_id is None or q_msg_id is None:
        await msg.reply('Error: Missing data in the state.\n Обратитесь с этой ошибкой к пользователю @user123')
        await state.clear()
        return

    rkb = make_reaction_keyboard(admin_chat_id=admin_chat_id,
                                 answer_msg_id=answer_msg_id,
                                 answer_msg_text=answer_msg_text,
                                 asker_id=data['asker_id'])

    response_message = [
        'Ответ от администратора:',
        msg.text,
        '\nПомог ли вам ответ?',
        '👍 – Да',
        '👎 – Нет',
    ]

    await bot.send_message(chat_id=support_chat_id, text='\n'.join(response_message), reply_to_message_id=q_msg_id,
                           reply_markup=rkb)
    await state.clear()
