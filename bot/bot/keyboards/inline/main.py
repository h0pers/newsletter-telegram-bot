from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class InlineButtonText:
    BACK_BUTTON = 'Назад ◀️'
    MAIN_PAGE_BUTTON = 'Главная страница 📟'
    CANCEL_BUTTON = 'Отменить ❌'
    DELETE_BUTTON = 'Удалить ❌'


class Inline:
    inline_buttons: List[List[InlineKeyboardButton]]
    markup: InlineKeyboardMarkup
    back_button = InlineKeyboardButton(text=InlineButtonText.BACK_BUTTON,
                                       callback_data='back')
    cancel_button = InlineKeyboardButton(text=InlineButtonText.CANCEL_BUTTON,
                                         callback_data='cancel')
    main_page_button = InlineKeyboardButton(text=InlineButtonText.MAIN_PAGE_BUTTON,
                                            callback_data='main_page')

    def __init__(self, buttons_list: List[List[InlineKeyboardButton]]):
        self.inline_buttons = buttons_list

    def get_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=self.inline_buttons)
