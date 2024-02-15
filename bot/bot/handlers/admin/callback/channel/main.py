from aiogram import Router

from .add_channel import add_channel_callback_router
from .control_channels import control_channels_callback_router
from .delete_channel import delete_channel_callback_router
from .available_channels import available_channels_callback_router

channel_callback_router = Router()


def get_channel_callback_callback_router() -> Router:
    channel_callback_routers = (control_channels_callback_router, add_channel_callback_router,
                                delete_channel_callback_router, available_channels_callback_router)
    channel_callback_router.include_routers(*channel_callback_routers)

    return channel_callback_router
