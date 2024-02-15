from aiogram.types import InlineKeyboardButton

from bot.keyboards.inline.main import Inline, InlineButtonText
from bot.callback.newsletter import NewsletterAction

from bot.callback.channels import ChannelsAction


class AdminInlineButtonText(InlineButtonText):
    CONTROL_CHANNELS = 'Управлять чатами 💬'
    CONTROL_NEWSLETTER = 'Управлять рассылкой 📰'
    AVAILABLE_NEWSLETTERS = 'Текущие рассылки 🚀'


control_newsletter = InlineKeyboardButton(text=AdminInlineButtonText.CONTROL_NEWSLETTER,
                                          callback_data=NewsletterAction(control_newsletter=1).pack())
control_channels = InlineKeyboardButton(text=AdminInlineButtonText.CONTROL_CHANNELS,
                                        callback_data=ChannelsAction(control_channel=1).pack())
available_newsletters = InlineKeyboardButton(text=AdminInlineButtonText.AVAILABLE_NEWSLETTERS,
                                             callback_data=NewsletterAction(edit_newsletter=1).pack())

admin_panel_markup = Inline([[control_newsletter, control_channels], [available_newsletters]])
