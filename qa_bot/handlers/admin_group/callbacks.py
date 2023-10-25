from aiogram import Bot, html, types
from aiogram.fsm.context import FSMContext

from qa_bot.keyboards.inline.callbacks import AnswerCallback
from qa_bot.states.admin_chat import AdminChatAnswerStates


async def write_answer_callback(callback_query: types.CallbackQuery, callback_data: AnswerCallback, bot: Bot,
                                state: FSMContext) -> None:
    admin_chat_id = callback_query.message.chat.id
    msg_to_edit = callback_query.message.message_id
    support_chat_id = callback_data.support_chat_id
    question_msg_id = callback_data.question_msg_id
    question_text = callback_query.message.entities[-1].extract_from(callback_query.message.text)
    asker_id = callback_data.asker_id

    admin_user_name = f"@{callback_query.from_user.username}" if callback_query.from_user.username else "Админ"

    current_state = await state.get_state()

    if current_state == AdminChatAnswerStates.write_answer:
        await callback_query.answer('Сперва ответьте на вопрос, который Вы взяли в обработку', show_alert=True)
        return

    await state.update_data(support_chat_id=support_chat_id, q_msg_id=question_msg_id, asker_id=asker_id)

    m = [
        f'{html.quote(admin_user_name)}, напишите ответ на вопрос и отправьте сообщение:',
        f'<code>{html.quote(question_text)}</code>'
    ]
    await bot.edit_message_text(text='\n'.join(m), chat_id=admin_chat_id, message_id=msg_to_edit)

    await state.set_state(AdminChatAnswerStates.write_answer)
    await callback_query.answer()
