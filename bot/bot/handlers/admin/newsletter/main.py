from aiogram import Router

from .set_newsletter_chat import set_newsletter_chat_router
from .set_newsletter_message import set_newsletter_message_router
from .control_time.main import get_control_time_router

newsletter_router = Router()


def get_newsletter_router() -> Router:
    newsletter_routers = (set_newsletter_chat_router, set_newsletter_message_router,
                          get_control_time_router(),)
    newsletter_router.include_routers(*newsletter_routers)
    return newsletter_router
