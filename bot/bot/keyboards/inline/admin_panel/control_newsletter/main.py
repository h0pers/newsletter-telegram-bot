from aiogram.types import InlineKeyboardButton

from bot.keyboards.inline.main import Inline, InlineButtonText

from bot.callback.newsletter import NewsletterAction


class NewsletterInlineButtonText(InlineButtonText):
    NEW_FORWARD = 'Создать новую рассылку 🆕'
    EDIT_NEWSLETTER = 'Остановить рассылку 🛃'


new_forward_message = InlineKeyboardButton(text=NewsletterInlineButtonText.NEW_FORWARD,
                                           callback_data=NewsletterAction(new_newsletter=1).pack())
available_newsletters = InlineKeyboardButton(text=NewsletterInlineButtonText.EDIT_NEWSLETTER,
                                             callback_data=NewsletterAction(edit_newsletter=1).pack())

control_newsletter_markup = Inline([[new_forward_message], [available_newsletters], [Inline.back_button]])
