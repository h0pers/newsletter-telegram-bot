from aiogram.filters.callback_data import CallbackData


class NewsletterAction(CallbackData, prefix="newsletter"):
    newsletter_id: int = 0
    newsletter_message_id: int = 0
    control_newsletter: int = 0
    edit_newsletter: int = 0
    new_newsletter: int = 0
    control_newsletter_time: int = 0
    set_newsletter_periodic_time: int = 0
    set_newsletter_time: int = 0
    set_newsletter_chat: int = 0
    set_newsletter_category: int = 0
    set_newsletter_message: int = 0
    publish_newsletter: int = 0
    delete_newsletter: int = 0


class NewsletterTypes(CallbackData, prefix="newsletter_type"):
    static_message: int = 0
    periodic_message: int = 0
