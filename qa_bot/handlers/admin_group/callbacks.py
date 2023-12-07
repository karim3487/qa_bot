from aiogram import Bot, types
from aiogram.fsm.context import FSMContext

from qa_bot.utils.messages import MESSAGES
from qa_bot.keyboards.inline.answer import (
    make_cancel_answer_keyboard,
    make_start_answer_keyboard,
)
from qa_bot.keyboards.inline.callbacks import (
    CancelAnsweringCallback,
    StartAnsweringCallback,
)


async def start_answering_callback(
    callback_query: types.CallbackQuery,
    callback_data: StartAnsweringCallback,
    bot: Bot,
    state: FSMContext,
) -> None:
    await state.update_data(msg_html=callback_query.message.html_text)
    username = callback_query.from_user.username

    if username:
        username = f"@{username}"
    else:
        username = callback_query.from_user.full_name

    m = MESSAGES.Info.add_instruction_to_question(
        callback_query.message.html_text,
        callback_data.support_chat_id,
        callback_data.q_msg_id,
        username,
    )

    rkb = make_cancel_answer_keyboard(
        answering_id=callback_query.from_user.id,
        support_chat_id=callback_data.support_chat_id,
        q_msg_id=callback_data.q_msg_id,
    )

    await bot.edit_message_text(
        m,
        callback_query.message.chat.id,
        callback_query.message.message_id,
        reply_markup=rkb,
    )

    await callback_query.answer()


async def cancel_answering_callback(
    callback_query: types.CallbackQuery,
    callback_data: CancelAnsweringCallback,
    bot: Bot,
    state: FSMContext,
) -> None:
    if callback_query.from_user.id != callback_data.answering_id:
        await callback_query.answer(MESSAGES.Errors.cancel_answering)
        return
    data = await state.get_data()

    rkb = make_start_answer_keyboard(
        support_chat_id=callback_data.support_chat_id, q_msg_id=callback_data.q_msg_id
    )

    await bot.edit_message_text(
        data["msg_html"],
        callback_query.message.chat.id,
        callback_query.message.message_id,
        reply_markup=rkb,
    )

    await callback_query.answer()
