from aiogram.fsm.state import StatesGroup, State


class StateUser(StatesGroup):
    first_name = State()
    last_name = State()

    email = State()
    city = State()

    show = State()
