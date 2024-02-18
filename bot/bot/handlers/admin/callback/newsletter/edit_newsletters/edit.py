from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callback.newsletter import NewsletterAction
from bot.fsm.newsletter import Newsletter
from bot.keyboards.inline.admin_panel.control_newsletter.available_newsletters.main import choose_newsletter_type

edit_newsletter_callback_router = Router()


@edit_newsletter_callback_router.callback_query(NewsletterAction.filter(F.edit_newsletter == 1))
async def edit_newsletter(query: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(Newsletter.edit_newsletter)
    await query.message.edit_reply_markup(reply_markup=choose_newsletter_type.get_markup())


