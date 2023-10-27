from aiogram.fsm.state import State, StatesGroup


class AdminChatAnswer(StatesGroup):
    write_question = State()
