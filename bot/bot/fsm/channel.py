from aiogram.fsm.state import StatesGroup, State


class Channel(StatesGroup):
    control_channel = State()
    new_channel = State()
    delete_channel = State()
