from aiogram import Bot, types
from aiogram.fsm.context import FSMContext

from qa_bot.data import config
from qa_bot.utils.api.answer import Answer
from qa_bot.utils.api.auto_responder_api import auto_responder_api as api
from qa_bot.keyboards.inline.reactions import make_reaction_keyboard
from qa_bot.utils.messages import MESSAGES
from qa_bot.keyboards.inline.answer import (
    make_cancel_answer_keyboard,
    make_start_answer_keyboard,
)
from qa_bot.keyboards.inline.callbacks import (
    CancelAnsweringCallback,
    StartAnsweringCallback,
    AnswerCallback,
)


async def show_kb_with_answers(msg: types.Message) -> None:
    entities = msg.entities[2:]
    for item in entities:
        item.extract_from(msg.text)


async def start_answering_callback(
    callback_query: types.CallbackQuery,
    callback_data: StartAnsweringCallback,
    bot: Bot,
    state: FSMContext,
) -> None:
    answers_id = eval(callback_data.answers_id)
    await show_kb_with_answers(callback_query.message)

    await state.update_data(
        msg_html=callback_query.message.html_text,
        q_msg_id=callback_data.q_msg_id,
        answers_id=answers_id,
    )

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
        answers_id=answers_id,
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
        support_chat_id=callback_data.support_chat_id,
        q_msg_id=callback_data.q_msg_id,
        answers_id=data["answers_id"],
    )

    await bot.edit_message_text(
        data["msg_html"],
        callback_query.message.chat.id,
        callback_query.message.message_id,
        reply_markup=rkb,
    )

    await callback_query.answer()


async def answer_button_callback(
    callback_query: types.CallbackQuery,
    callback_data: AnswerCallback,
    bot: Bot,
    state: FSMContext,
) -> None:
    msg = callback_query.message

    data = await state.get_data()
    q_msg_id = data["q_msg_id"]

    support_chat_id = config.SUPPORT_CHAT_ID
    question_msg_id = q_msg_id
    answer = Answer.from_dict(await api.get_answer(callback_data.answer_id))

    rkb = make_reaction_keyboard(
        admin_chat_id=config.ADMIN_CHAT_ID, answer_msg_id=msg.message_id
    )

    await bot.send_message(
        chat_id=support_chat_id,
        text=MESSAGES.Info.AnswerWithReactions.from_admin(answer.text),
        reply_to_message_id=question_msg_id,
        reply_markup=rkb,
    )

    await bot.edit_message_text(
        MESSAGES.Info.add_sent_status(
            msg.html_text,
        ),
        msg.chat.id,
        msg.message_id,
    )
    await callback_query.answer()
