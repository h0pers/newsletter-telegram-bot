from aiogram import Router

from .admin_panel import admin_panel_router
from .callback.main import get_admin_callback_router
from .channel.main import get_channel_router
from .newsletter.main import get_newsletter_router
from .category.main import get_category_router

from bot.filters.is_admin import OnlyAdmin, OnlyAdminCallback
from bot.middleware.collect_data import CollectData


admin_router = Router()

admin_router.message.middleware(CollectData())

admin_router.message.filter(OnlyAdmin())
admin_router.callback_query.filter(OnlyAdminCallback())


def get_admin_router() -> Router:
    admin_routers = (admin_panel_router, get_admin_callback_router(), get_channel_router(),
                     get_newsletter_router(), get_category_router())
    admin_router.include_routers(*admin_routers)
    return admin_router
