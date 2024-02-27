from typing import Dict, Optional, Tuple

from qa_bot.data import config
from qa_bot.utils.api.base import BaseClient
from qa_bot.utils.enums import TypeOfMessages
from qa_bot.utils.exceptions import AnswerAlreadyExists


class AutoResponderAPI(BaseClient):
    def __init__(self, answers_per_page: int = 5):
        self.answers_per_page = answers_per_page
        super().__init__(
            base_url=config.AUTORESPONDER_BASE_URL, api_key=config.AUTORESPONDER_API_KEY
        )

    async def get_answer_to_question(
        self, question: str
    ) -> Tuple[TypeOfMessages, Optional[str]]:
        url = f"/api/v1/answers/?cosine={question}"

        response = await self._make_authenticated_request(method="get", url=url)
        detail = response[1].get("detail")
        if response[0] == 400:
            if detail == "Is not a question":
                self.log.debug(f"It is not a question: {question}")
                return TypeOfMessages.IS_NO_Q, None
        if response[0] == 200 and response[1].get("count") == 3:
            self.log.debug(f"No answer to question: {question}")
            return TypeOfMessages.IS_Q_WITHOUT_ANSWER, response[1]["results"]
        return TypeOfMessages.IS_Q_WITH_ANSWER, response[1]["results"][0]["text"]

    async def add_answer(self, answer) -> None:
        url = "/api/v1/answers/"

        json = {"text": answer, "campaign": 1, "language": 2}
        response = await self._make_authenticated_request(
            method="post", url=url, json=json
        )
        if response[0] == 409:
            self.log.debug(f"An answer with this text already exists: {answer}")
            raise AnswerAlreadyExists

    async def get_answers(self, offset=0) -> Dict:
        limit = self.answers_per_page
        url = f"/api/v1/answers/?limit={limit}&offset={offset}"

        response = await self._make_authenticated_request(method="get", url=url)
        return response[1]

    async def get_answer(self, answer_id: int) -> Dict:
        url = f"/api/v1/answers/{answer_id}"
        response = await self._make_authenticated_request(method="get", url=url)
        return response[1]


auto_responder_api = AutoResponderAPI()
