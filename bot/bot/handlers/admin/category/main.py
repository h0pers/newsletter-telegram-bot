from aiogram import Router

from .new_category import new_category_router

category_router = Router()


def get_category_router() -> Router:
    category_routers = (new_category_router, )
    category_router.include_routers(*category_routers)
    return category_router
