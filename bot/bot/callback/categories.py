from aiogram.filters.callback_data import CallbackData


class CategoriesAction(CallbackData, prefix="categories_action"):
    control_categories: int = 0
    new_category: int = 0
    delete_category: int = 0
    available_category: int = 0


class Category(CallbackData, prefix="category"):
    category_id: int
    name: str
