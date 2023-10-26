from aiogram import Bot, html, types
from aiogram.filters import CommandObject

from qa_bot.data import config
from qa_bot.keyboards.inline.reactions import make_reaction_keyboard


async def answer_the_question(msg: types.Message, command: CommandObject, bot: Bot) -> None:
    if msg.from_user is None:
        return

    if not command.args:
        await msg.reply("Вы ввели что-то не то, попробуйте еще раз")

    args = command.args.split(' ', 2)

    if len(args) >= 3:
        support_chat_id = args.pop(0)
        question_msg_id = int(args.pop(0))
        answer = ' '.join(args)

        m = [
            'Ответ от администратора:',
            f'<code>{html.quote(answer)}</code>',
            '\nПомог ли вам ответ?',
            '👍 – Да',
            '👎 – Нет',
        ]
        rkb = make_reaction_keyboard(admin_chat_id=config.ADMIN_CHAT_ID,
                                     answer_msg_id=msg.message_id)

        await bot.send_message(chat_id=support_chat_id, text='\n'.join(m), reply_to_message_id=question_msg_id,
                               reply_markup=rkb)

        m = [
            '✅ Вы успешно ответили на вопрос!',
        ]
        await msg.reply('\n'.join(m))
        return
    else:
        m = [
            'Укажите аргументы команды',
            f'Пример: {html.code("/ответ 516712732 12 Ваш_ответ")}',
        ]
        await msg.reply('\n'.join(m))
        return
