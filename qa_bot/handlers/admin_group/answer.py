from aiogram import Bot, types
from aiogram.filters import CommandObject

from qa_bot.utils.messages import MESSAGES_RU, MESSAGES_KY
from qa_bot.data import config
from qa_bot.keyboards.inline.reactions import make_reaction_keyboard
from qa_bot.utils.my_services import clean_msg, detect_language


async def answer_the_question(
    msg: types.Message, command: CommandObject, bot: Bot
) -> None:
    if msg.from_user is None:
        return

    if not msg.reply_to_message:
        await msg.reply(MESSAGES_RU.Errors.AnswerToTheQuestion.did_not_reply_to_the_msg)
        return

    if not command.args:
        await msg.reply(MESSAGES_RU.Errors.AnswerToTheQuestion.no_args)

    args = command.args.split(" ", 2)

    if len(args) >= 2:
        support_chat_id = config.SUPPORT_CHAT_ID
        question_msg_id = int(args.pop(0))
        answer = " ".join(args)
        answer_language = detect_language(answer)

        rkb = make_reaction_keyboard(
            admin_chat_id=config.ADMIN_CHAT_ID, answer_msg_id=msg.message_id
        )

        if answer_language == "ky":
            m = MESSAGES_KY.Info.AnswerWithReactions.from_admin(answer)
        else:
            m = MESSAGES_RU.Info.AnswerWithReactions.from_admin(answer)

        await bot.send_message(
            chat_id=support_chat_id,
            text=m,
            reply_to_message_id=question_msg_id,
            reply_markup=rkb,
        )

        await clean_msg(msg.reply_to_message, msg.from_user, answer)

        return
    else:
        await msg.reply(MESSAGES_RU.Errors.AnswerToTheQuestion.incorrect_args)
        return
