from aiogram.types import InlineKeyboardButton

from bot.keyboards.inline.main import Inline, InlineButtonText

from bot.callback.newsletter import NewsletterAction
from bot.callback.categories import CategoriesAction


class NewsletterInlineButtonText(InlineButtonText):
    NEW_FORWARD = 'Создать новую рассылку 🆕'
    EDIT_NEWSLETTER = 'Остановить рассылку 🛃'
    CONTROL_CATEGORIES = 'Управлять категориями 📓'


new_forward_message = InlineKeyboardButton(text=NewsletterInlineButtonText.NEW_FORWARD,
                                           callback_data=NewsletterAction(new_newsletter=1).pack())
available_newsletters = InlineKeyboardButton(text=NewsletterInlineButtonText.EDIT_NEWSLETTER,
                                             callback_data=NewsletterAction(edit_newsletter=1).pack())
control_categories = InlineKeyboardButton(text=NewsletterInlineButtonText.CONTROL_CATEGORIES,
                                          callback_data=CategoriesAction(control_categories=1).pack())

control_newsletter_markup = Inline([[new_forward_message], [available_newsletters], [control_categories], [Inline.back_button]])
