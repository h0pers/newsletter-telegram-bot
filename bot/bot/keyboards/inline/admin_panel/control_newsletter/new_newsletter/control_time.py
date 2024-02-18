from aiogram.types import InlineKeyboardButton

from bot.keyboards.inline.main import Inline, InlineButtonText
from bot.callback.newsletter import NewsletterAction


class NewsletterTimeInlineButtonText(InlineButtonText):
    STATIC = 'Точное время 🕛'
    PERIODIC = 'Интервал 🧩'


static_time = InlineKeyboardButton(text=NewsletterTimeInlineButtonText.STATIC,
                                   callback_data=NewsletterAction(set_newsletter_time=1).pack())
periodic_time = InlineKeyboardButton(text=NewsletterTimeInlineButtonText.PERIODIC,
                                     callback_data=NewsletterAction(set_newsletter_periodic_time=1).pack())

control_time_markup = Inline([[static_time, periodic_time],
                              [Inline.back_button]])
