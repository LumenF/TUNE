from aiogram.fsm.state import StatesGroup, State


class StateBudget(StatesGroup):
    dia = State()
    show = State()
