from aiogram.types import InlineKeyboardButton

from bot.keyboards.inline.main import Inline, InlineButtonText

from bot.callback.channels import ChannelsAction


class ChannelsInlineButtonText(InlineButtonText):
    NEW_CHANNEL = 'Добавить канал 🆕'
    DELETE_CHANNEL = 'Удалить канал 🔴'
    AVAILABLE_CHANNELS = 'Доступные каналы 💬'


new_channel = InlineKeyboardButton(text=ChannelsInlineButtonText.NEW_CHANNEL,
                                   callback_data=ChannelsAction(new_channel=1).pack())
delete_channel = InlineKeyboardButton(text=ChannelsInlineButtonText.DELETE_CHANNEL,
                                      callback_data=ChannelsAction(delete_channel=1).pack())
available_channels = InlineKeyboardButton(text=ChannelsInlineButtonText.AVAILABLE_CHANNELS,
                                          callback_data=ChannelsAction(view_available_channels=1).pack())

control_channels_markup = Inline([[new_channel], [delete_channel, available_channels], [Inline.back_button]])
