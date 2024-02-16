from aiogram import Router

from .control_categories import control_categories_callback_router
from .new_category import new_category_callback_router
from .available_categories import available_categories_callback_router

categories_callback_router = Router()


def get_categories_callback_callback_router() -> Router:
    categories_callback_routers = (control_categories_callback_router, new_category_callback_router,
                                   available_categories_callback_router)
    categories_callback_router.include_routers(*categories_callback_routers)

    return categories_callback_router
