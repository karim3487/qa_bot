from aiogram import Bot, types
from aiogram.fsm.context import FSMContext

from qa_bot.utils.messages import MESSAGES
from qa_bot.keyboards.inline.answer import make_start_answer_keyboard
from qa_bot.keyboards.inline.callbacks import ReactionCallback
from qa_bot.states.support_chat import SupportChatQuestionStates


async def reaction_on_answer_callback(
    callback_query: types.CallbackQuery,
    callback_data: ReactionCallback,
    bot: Bot,
    state: FSMContext,
) -> None:
    asker_id = callback_query.message.reply_to_message.from_user.id
    user_id = callback_query.from_user.id
    support_chat_id = callback_query.message.chat.id
    answer_msg = callback_query.message
    answer_msg_id = answer_msg.message_id
    answer_text = answer_msg.entities[-1].extract_from(callback_query.message.text)
    question_text = answer_msg.reply_to_message.text
    question_msg_id = answer_msg.reply_to_message.message_id

    if asker_id != user_id:
        await callback_query.answer(MESSAGES.Errors.question_from_another_user)
        return
    # Reaction on message with answer from API
    if not callback_data.answer_msg_id:
        if callback_data.is_help:
            await bot.edit_message_text(
                MESSAGES.Info.ResponseFromApi.ok(answer_text),
                chat_id=support_chat_id,
                message_id=answer_msg_id,
            )
        else:
            await bot.edit_message_text(
                MESSAGES.Info.ResponseFromApi.nok(answer_text),
                chat_id=support_chat_id,
                message_id=answer_msg_id,
            )

            rkb = make_start_answer_keyboard(
                support_chat_id=support_chat_id, q_msg_id=question_msg_id
            )
            await bot.send_message(
                chat_id=callback_data.admin_chat_id,
                text=MESSAGES.Info.question_after_reaction(question_text, answer_text),
                reply_markup=rkb,
            )
            await callback_query.answer()
    # Reaction on message with answer from admin
    else:
        if callback_data.is_help:
            await bot.edit_message_text(
                MESSAGES.Info.ResponseFromAdmin.ok(answer_text),
                chat_id=support_chat_id,
                message_id=answer_msg_id,
            )
        else:
            await state.set_state(SupportChatQuestionStates.write_question)
            await bot.edit_message_text(
                MESSAGES.Info.ResponseFromAdmin.nok(answer_text),
                chat_id=support_chat_id,
                message_id=answer_msg_id,
            )

        await callback_query.answer()
