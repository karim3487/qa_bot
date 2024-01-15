class Answer:
    def __init__(self, answer_id, text, english_text, language):
        self.answer_id = answer_id
        self.text = text
        self.english_txt = english_text
        self.language = language

    @classmethod
    def from_dict(cls, data):
        return cls(
            answer_id=data.get("id"),
            text=data.get("text"),
            english_text=data.get("english_text"),
            language=data.get("language"),
        )
