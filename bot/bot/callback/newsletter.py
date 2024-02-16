from aiogram.filters.callback_data import CallbackData


class NewsletterAction(CallbackData, prefix="newsletter"):
    control_newsletter: int = 0
    edit_newsletter: int = 0
    new_newsletter: int = 0
    set_newsletter_time: int = 0
    set_newsletter_chat: int = 0
    set_newsletter_message: int = 0
    publish_newsletter: int = 0
    delete_newsletter: int = 0
    set_category: int = 0
