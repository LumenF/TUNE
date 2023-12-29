from aiogram.fsm.state import StatesGroup, State


class StateSupp(StatesGroup):
    type = State()
    manufacturer = State()
    category = State()
    subcategory = State()

    show = State()
