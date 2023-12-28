class Answer:
    def __init__(self, text, english_text, language):
        self.text = text
        self.english_txt = english_text
        self.language = language

    @classmethod
    def from_dict(cls, data):
        return cls(
            text=data.get("text"),
            english_text=data.get("english_text"),
            language=data.get("language"),
        )
