from aiogram import html, types
from aiogram.fsm.context import FSMContext

from qa_bot.utils.api.answer import Answer
from qa_bot.utils.messages import MESSAGES_RU, MESSAGES_KY
from qa_bot.data import config
from qa_bot.keyboards.inline.answer import make_start_answer_keyboard
from qa_bot.keyboards.inline.reactions import make_reaction_keyboard
from qa_bot.utils.api.auto_responder_api import auto_responder_api
from qa_bot.utils.enums import TypeOfMessages
from qa_bot.utils.my_services import detect_language

def get_waiting_msg(language: str) -> str:
    if language == "ky":
        return MESSAGES_KY.Info.waiting
    else:
        return MESSAGES_RU.Info.waiting


async def new_msg_in_group(msg: types.Message, state: FSMContext) -> None:
    if msg.from_user is None:
        return

    question_text = msg.text
    question_language = detect_language(question_text)
    question_msg_id = msg.message_id
    admin_chat_id = config.ADMIN_CHAT_ID
    username_url = f'<a href="tg://user?id={msg.from_user.id}">{html.quote(msg.from_user.full_name)}</a>'

    message_type, result = await auto_responder_api.get_answer_to_question(
        question_text
    )
    if message_type == TypeOfMessages.IS_Q_WITH_ANSWER:
        answer_text = result
        rkb = make_reaction_keyboard(
            admin_chat_id=admin_chat_id, q_msg_id=question_msg_id
        )
        if question_language == "ky":
            m = MESSAGES_KY.Info.AnswerWithReactions.from_api(answer_text)
        else:
            m = MESSAGES_RU.Info.AnswerWithReactions.from_api(answer_text)

        await msg.reply(m, reply_markup=rkb)

    elif message_type == TypeOfMessages.IS_Q_WITHOUT_ANSWER:
        answers = [Answer.from_dict(item) for item in result]
        rkb = make_start_answer_keyboard(
            q_msg_id=msg.message_id,
            answers_id=[a.answer_id for a in answers],
        )

        m = get_waiting_msg(question_language)
        await msg.reply(m)

        await msg.bot.send_message(
            chat_id=admin_chat_id,
            text=MESSAGES_RU.Info.question_without_answer(
                username_url, msg.text, [a.text for a in answers]
            ),
            reply_markup=rkb,
        )


async def last_question(msg: types.Message, state: FSMContext):
    admin_chat_id = config.ADMIN_CHAT_ID
    username_url = f'<a href="tg://user?id={msg.from_user.id}">{html.quote(msg.from_user.full_name)}</a>'
    rkb = make_start_answer_keyboard(q_msg_id=msg.message_id)
    question_language = detect_language(msg.text)

    m = get_waiting_msg(question_language)
    await msg.reply(m)

    await msg.bot.send_message(
        chat_id=admin_chat_id,
        text=MESSAGES_RU.Info.another_question(username_url, msg.text),
        reply_markup=rkb,
    )
    await state.clear()
