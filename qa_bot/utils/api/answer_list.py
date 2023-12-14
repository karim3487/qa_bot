import asyncio

from qa_bot.utils.api.auto_responder_api import auto_responder_api


class AnswerList:
    _instance = None

    def __new__(cls, data, answers_per_page=5):
        if not cls._instance:
            cls._instance = super(AnswerList, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, data, answers_per_page=5):
        if not self._initialized:
            self.count_answers = data.get("count", 0)
            self.next_page = data.get("next")
            self.previous_page = data.get("previous")
            self.answers = [Answer(result) for result in data.get("results", [])]
            self.answers_per_page = answers_per_page

            self.offset = 0
            self.current_page = 1
            self._initialized = True

    @property
    def total_pages(self):
        total_pages = self.count_answers // self.answers_per_page
        if self.count_answers % self.answers_per_page > 0:
            total_pages += 1
        return total_pages

    async def get_next_page_answers(self):
        if self.next_page:
            self.offset = int(self.next_page.split("offset=")[1])
            new_data = await auto_responder_api.get_answers(self.offset)
            self.current_page += 1

            self.count_answers = new_data.get("count", 0)
            self.next_page = new_data.get("next")
            self.previous_page = new_data.get("previous")
            self.answers = [Answer(result) for result in new_data.get("results", [])]
        else:
            return None

    async def go_to_page(self, page):
        self.offset = page * self.answers_per_page - self.answers_per_page
        new_data = await auto_responder_api.get_answers(self.offset)
        self.current_page = page

        self.count_answers = new_data.get("count", 0)
        self.next_page = new_data.get("next")
        self.previous_page = new_data.get("previous")
        self.answers = [Answer(result) for result in new_data.get("results", [])]


class Answer:
    def __init__(self, answer_data):
        self.id = answer_data.get("id")
        self.text = answer_data.get("text")
        self.english_text = answer_data.get("english_text")
