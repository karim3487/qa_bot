from aiogram import Bot, html, types
from aiogram.fsm.context import FSMContext

from qa_bot.keyboards.inline.reactions import make_reaction_keyboard


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
                                 asker_id=data['asker_id'])

    response_message = [
        'Ответ от администратора:',
        f'<code>{html.quote(answer_msg_text)}</code>',
        '\nПомог ли вам ответ?',
        '👍 – Да',
        '👎 – Нет',
    ]

    await bot.send_message(chat_id=support_chat_id, text='\n'.join(response_message), reply_to_message_id=q_msg_id,
                           reply_markup=rkb)
    await state.clear()
