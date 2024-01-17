from aiogram import Bot, types
from aiogram.filters import CommandObject

from qa_bot.utils.messages import MESSAGES
from qa_bot.data import config
from qa_bot.keyboards.inline.reactions import make_reaction_keyboard


async def answer_the_question(
    msg: types.Message, command: CommandObject, bot: Bot
) -> None:
    if msg.from_user is None:
        return

    if not msg.reply_to_message:
        await msg.reply(MESSAGES.Errors.AnswerToTheQuestion.did_not_reply_to_the_msg)
        return

    if not command.args:
        await msg.reply(MESSAGES.Errors.AnswerToTheQuestion.no_args)

    args = command.args.split(" ", 2)

    if len(args) >= 2:
        support_chat_id = config.SUPPORT_CHAT_ID
        question_msg_id = int(args.pop(0))
        answer = " ".join(args)

        rkb = make_reaction_keyboard(
            admin_chat_id=config.ADMIN_CHAT_ID, answer_msg_id=msg.message_id
        )

        await bot.send_message(
            chat_id=support_chat_id,
            text=MESSAGES.Info.AnswerWithReactions.from_admin(answer),
            reply_to_message_id=question_msg_id,
            reply_markup=rkb,
        )

        await bot.edit_message_text(
            MESSAGES.Info.add_sent_status(
                msg.reply_to_message.html_text,
            ),
            msg.chat.id,
            msg.reply_to_message.message_id,
        )

        return
    else:
        await msg.reply(MESSAGES.Errors.AnswerToTheQuestion.incorrect_args)
        return
