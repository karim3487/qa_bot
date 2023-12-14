from aiogram.fsm.state import State, StatesGroup


class SupportChatQuestionStates(StatesGroup):
    write_question = State()

class Test(StatesGroup):
    test = State()
