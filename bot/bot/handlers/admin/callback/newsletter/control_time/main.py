from aiogram import Router

from .set_newsletter_time import set_newsletter_time_callback_router
from .control_newsletter_time import control_newsletter_time_callback_router
from .set_periodic_time import set_periodic_time_callback_router

control_time_callback_router = Router()


def get_control_time_callback_router() -> Router:
    control_time_callback_routers = (set_newsletter_time_callback_router, control_newsletter_time_callback_router,
                                     set_periodic_time_callback_router)
    control_time_callback_router.include_routers(*control_time_callback_routers)

    return control_time_callback_router
