from aiogram.fsm.state import StatesGroup, State


class StateMail(StatesGroup):
    show = State()


class QuizState(StatesGroup):
    next = State()
    finish = State()