from aiogram import Router

from .edit import edit_newsletter_callback_router

edit_newsletters_callback_router = Router()


def get_edit_newsletters_callback_router() -> Router:
    edit_newsletters_callback_routers = (edit_newsletter_callback_router,)
    edit_newsletters_callback_router.include_routers(*edit_newsletters_callback_routers)

    return edit_newsletters_callback_router
