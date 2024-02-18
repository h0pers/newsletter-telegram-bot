from aiogram.types import InlineKeyboardButton

from bot.keyboards.inline.main import Inline, InlineButtonText
from bot.callback.categories import CategoriesAction


class CategoriesInlineButtonText(InlineButtonText):
    NEW_CATEGORY = 'Новая категория 🆕'
    DELETE_CATEGORY = 'Удалить категорию 🔴'
    AVAILABLE_CATEGORIES = 'Доступные категории 📃'


create_category = InlineKeyboardButton(text=CategoriesInlineButtonText.NEW_CATEGORY,
                                       callback_data=CategoriesAction(new_category=1).pack())
delete_category = InlineKeyboardButton(text=CategoriesInlineButtonText.DELETE_CATEGORY,
                                       callback_data=CategoriesAction(delete_category=1).pack())

available_categories = InlineKeyboardButton(text=CategoriesInlineButtonText.AVAILABLE_CATEGORIES,
                                            callback_data=CategoriesAction(available_category=1).pack())

control_categories_markup = Inline(
    [[create_category, delete_category],
     [available_categories],
     [Inline.back_button]]
)
