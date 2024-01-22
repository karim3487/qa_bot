from aiogram import types, html
from google.cloud import translate_v2 as translate

from qa_bot.utils.messages import MESSAGES_RU


def detect_language(text: str) -> str:
    """Return language short name"""
    translate_client = translate.Client()
    return translate_client.detect_language(text)["language"]


def make_user_url(user: types.User) -> str:
    return f'<a href="tg://user?id={user.id}">{html.quote(user.full_name)}</a>'


async def clean_msg(
    msg: types.Message, answering: types.User, answer_text: str
) -> None:
    asker = msg.entities[0].user
    asker_username_url = make_user_url(asker)
    answering_username_url = make_user_url(answering)

    question = msg.entities[1].extract_from(msg.text)

    await msg.edit_text(
        MESSAGES_RU.Info.cleared_message(
            asker_username_url, answering_username_url, question, answer_text
        )
    )
