from aiogram.filters.callback_data import CallbackData


class ChannelsAction(CallbackData, prefix="channel"):
    primary_chat_id: int = 0
    control_channel: int = 0
    new_channel: int = 0
    delete_channel: int = 0
    view_available_channels: int = 0
