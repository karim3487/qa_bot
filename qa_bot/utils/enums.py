from enum import Enum


class TypeOfMessages(Enum):
    IS_Q_WITH_ANSWER = 1
    IS_Q_WITHOUT_ANSWER = 2
    IS_NO_Q = 3
