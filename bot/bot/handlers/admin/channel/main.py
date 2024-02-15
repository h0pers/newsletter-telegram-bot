from aiogram import Router

from .add_channel import add_channel_router

channel_router = Router()


def get_channel_router() -> Router:
    channel_routers = (add_channel_router, )
    channel_router.include_routers(*channel_routers)
    return channel_router
