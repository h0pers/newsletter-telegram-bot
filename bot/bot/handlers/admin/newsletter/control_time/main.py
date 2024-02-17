from aiogram import Router

from .set_newsletter_period_time import set_newsletter_period_time_message_router
from .set_newsletter_time import set_newsletter_time_router

control_time_message_router = Router()


def get_control_time_router() -> Router:
    control_time_message_routers = (set_newsletter_period_time_message_router, set_newsletter_time_router)
    control_time_message_router.include_routers(*control_time_message_routers)
    return control_time_message_router
