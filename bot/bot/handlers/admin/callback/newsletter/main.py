from aiogram import Router

from .control_newsletter import control_newsletter_callback_router
from .new_newsletter import new_newsletter_callback_router
from .edit_newsletter import edit_newsletter_callback_router
from .set_newsletter_chat import set_newsletter_chat_callback_router
from .set_newsletter_message import set_newsletter_message_callback_router
from .set_newsletter_time import set_newsletter_time_callback_router
from .publish_newsletter import publish_callback_router

newsletter_callback_router = Router()


def get_newsletter_callback_router() -> Router:
    newsletter_callback_routers = (control_newsletter_callback_router, new_newsletter_callback_router,
                                   edit_newsletter_callback_router, set_newsletter_chat_callback_router,
                                   set_newsletter_message_callback_router, set_newsletter_time_callback_router,
                                   publish_callback_router)
    newsletter_callback_router.include_routers(*newsletter_callback_routers)

    return newsletter_callback_router
