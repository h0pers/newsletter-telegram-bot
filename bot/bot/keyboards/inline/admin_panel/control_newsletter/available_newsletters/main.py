from aiogram.types import InlineKeyboardButton

from bot.keyboards.inline.main import Inline, InlineButtonText
from bot.callback.newsletter import NewsletterTypes


class AvailableNewsletterInlineButtonText(InlineButtonText):
    STATIC_MESSAGES = 'По времени 🕛'
    PERIODIC_MESSAGES = 'Интервальная рассылка 🧩'


static_messages = InlineKeyboardButton(text=AvailableNewsletterInlineButtonText.STATIC_MESSAGES,
                                       callback_data=NewsletterTypes(static_message=1).pack())
periodic_messages = InlineKeyboardButton(text=AvailableNewsletterInlineButtonText.PERIODIC_MESSAGES,
                                         callback_data=NewsletterTypes(periodic_message=1).pack())

choose_newsletter_type = Inline([[static_messages], [periodic_messages], [Inline.main_page_button]])
