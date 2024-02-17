from aiogram import Router

from .static_newsletter import static_newsletter_callback_router
from .periodic_newsletter import periodic_newsletter_callback_router

newsletter_types_callback_router = Router()


def get_newsletter_types_callback_router() -> Router:
    newsletter_types_callback_routers = (static_newsletter_callback_router, periodic_newsletter_callback_router)
    newsletter_types_callback_router.include_routers(*newsletter_types_callback_routers)

    return newsletter_types_callback_router
