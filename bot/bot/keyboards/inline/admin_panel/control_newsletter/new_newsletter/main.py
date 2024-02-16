from aiogram.types import InlineKeyboardButton

from bot.keyboards.inline.main import Inline, InlineButtonText

from bot.callback.newsletter import NewsletterAction


class NewNewsletterInlineButtonText(InlineButtonText):
    SET_TIME = 'Установить время 🕛'
    SET_CHAT = 'Установить чат отправки 💬'
    SET_MESSAGE = 'Установить сообщение 📨'
    SET_CATEGORY = 'Установить категорию 📃'
    SEND_NEWSLETTER = 'Отправить сообщение 🛫'


set_newsletter_time = InlineKeyboardButton(text=NewNewsletterInlineButtonText.SET_TIME,
                                           callback_data=NewsletterAction(set_newsletter_time=1).pack())
set_newsletter_chat = InlineKeyboardButton(text=NewNewsletterInlineButtonText.SET_CHAT,
                                           callback_data=NewsletterAction(set_newsletter_chat=1).pack())
set_newsletter_message = InlineKeyboardButton(text=NewNewsletterInlineButtonText.SET_MESSAGE,
                                              callback_data=NewsletterAction(set_newsletter_message=1).pack())
set_category = InlineKeyboardButton(text=NewNewsletterInlineButtonText.SET_CATEGORY,
                                    callback_data=NewsletterAction(set_category=1).pack())
publish_newsletter_message = InlineKeyboardButton(text=NewNewsletterInlineButtonText.SEND_NEWSLETTER,
                                                  callback_data=NewsletterAction(publish_newsletter=1).pack())

new_newsletter_markup = Inline([[set_newsletter_chat, set_newsletter_message],
                                [set_newsletter_time, set_category],
                                [publish_newsletter_message],
                                [Inline.back_button]])
