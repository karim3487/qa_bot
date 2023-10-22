from aiogram.fsm.state import State, StatesGroup


class AdminChatAnswerStates(StatesGroup):
    write_answer = State()
