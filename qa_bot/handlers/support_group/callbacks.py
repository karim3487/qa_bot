from aiogram import Bot, types
from aiogram.fsm.context import FSMContext

from qa_bot.utils.messages import MESSAGES
from qa_bot.keyboards.inline.answer import make_start_answer_keyboard
from qa_bot.keyboards.inline.callbacks import ReactionCallback
from qa_bot.states.support_chat import SupportChatQuestionStates


def extract_answer_text(answer_msg: types.Message) -> str:
    entities = answer_msg.entities
    # filtered_entities = [entity for entity in entities if entity.type != 'italic']
    # for entity in entities:
    #     for f_entity in filtered_entities:
    #         if f_entity.offset == entity.offset and f_entity.type != entity.type:
    #             entities.remove(entity)

    filtered_entities = [entity for entity in entities if entity.type != "italic"]
    unique_entities = {entity.offset: entity for entity in entities}
    entities = list(unique_entities.values())

    m = ""
    for item in entities:
        m += item.extract_from(answer_msg.text)
    return m


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
    answer_text = extract_answer_text(answer_msg)
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

            rkb = make_start_answer_keyboard(q_msg_id=question_msg_id)
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
