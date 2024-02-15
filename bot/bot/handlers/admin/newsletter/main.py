from aiogram import Router

from .set_newsletter_chat import set_newsletter_chat_router
from .set_newsletter_message import set_newsletter_message_router
from .set_newsletter_time import set_newsletter_time_router

newsletter_router = Router()


def get_newsletter_router() -> Router:
    newsletter_routers = (set_newsletter_chat_router, set_newsletter_message_router,
                          set_newsletter_time_router,)
    newsletter_router.include_routers(*newsletter_routers)
    return newsletter_router
