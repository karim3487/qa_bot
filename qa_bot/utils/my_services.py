from aiogram import types, html


def make_user_url(user: types.User) -> str:
    return f'<a href="tg://user?id={user.id}">{html.quote(user.full_name)}</a>'


async def clean_msg(
    msg: types.Message, answering: types.User, answer_text: str
) -> None:
    asker = msg.entities[0].user
    username_url = make_user_url(asker)

    question = msg.entities[1].extract_from(msg.text)

    m = [
        f"Пользователь {username_url} задал вопрос:",
        html.code(html.quote(question)),
        f"\n✅ На него ответил администратор {make_user_url(answering)}:",
        f"{html.quote(answer_text)}",
    ]

    await msg.edit_text("\n".join(m))
