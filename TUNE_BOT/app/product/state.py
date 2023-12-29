from aiogram.fsm.state import StatesGroup, State


class StateNew(StatesGroup):
    type = State()
    manufacturer = State()
    category = State()
    subcategory = State()

    keys = State()
    show = State()
