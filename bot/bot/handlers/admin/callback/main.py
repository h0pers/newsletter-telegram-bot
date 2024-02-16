from aiogram import Router

from bot.middleware.collect_data import CollectCallbackData

from .channel.main import get_channel_callback_callback_router
from .newsletter.main import get_newsletter_callback_router
from .categories.main import get_categories_callback_callback_router
from .main_page import main_page_callback_router

admin_callback_router = Router()
admin_callback_router.callback_query.middleware(CollectCallbackData())


def get_admin_callback_router() -> Router:
    admin_callback_routers = (get_newsletter_callback_router(), get_channel_callback_callback_router(),
                              get_categories_callback_callback_router(), main_page_callback_router, )
    admin_callback_router.include_routers(*admin_callback_routers)

    return admin_callback_router
