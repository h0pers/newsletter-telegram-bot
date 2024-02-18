from aiogram.fsm.state import StatesGroup, State


class Categories(StatesGroup):
    control_categories = State()
    new_category = State()
    available_categories = State()
    delete_category = State()
