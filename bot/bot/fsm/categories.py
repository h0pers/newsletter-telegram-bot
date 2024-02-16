from aiogram.fsm.state import StatesGroup, State


class Categories(StatesGroup):
    control_categories = State()
    new_category = State()
    delete_category = State()
