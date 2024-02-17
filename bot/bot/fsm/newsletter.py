from aiogram.fsm.state import StatesGroup, State


class Newsletter(StatesGroup):
    control_newsletter = State()
    edit_newsletter = State()
    edit_static_newsletter = State()
    edit_periodic_newsletter = State()
    new_newsletter = State()
    set_newsletter_time = State()
    set_newsletter_periodic_time = State()
    set_newsletter_chat = State()
    set_newsletter_message = State()
    control_newsletter_time = State()

