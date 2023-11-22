from typing import Optional, Mapping, Tuple

from qa_bot.data import config
from qa_bot.utils.api.base import BaseClient
from qa_bot.utils.enums import TypeOfMessages


class AutoResponderAPI(BaseClient):
    def __init__(self):
        super().__init__(
            base_url=config.AUTORESPONDER_BASE_URL, api_key=config.AUTORESPONDER_API_KEY
        )

    async def get_answer_to_question(
        self, question: str
    ) -> Tuple[TypeOfMessages, Optional[str]]:
        url = f"/api/v1/answers/?cosine={question}"

        response = await self._make_authenticated_request(method="get", url=url)
        if response[0] == 400:
            detail = response[1]["detail"]
            if detail == "Is not a question":
                return TypeOfMessages.IS_NO_Q, None
            if detail == "No answer to the question":
                return TypeOfMessages.IS_Q_WITHOUT_ANSWER, None
        return TypeOfMessages.IS_Q_WITH_ANSWER, response[1]["results"][0]["text"]

    async def add_answer(self, answer) -> None:
        url = "/api/v1/answers/"

        json = {"text": answer, "campaign": 1, "language": 2}
        response = await self._make_authenticated_request(
            method="post", url=url, json=json
        )


auto_responder_api = AutoResponderAPI()
