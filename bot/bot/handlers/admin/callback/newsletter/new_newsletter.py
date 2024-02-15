from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.keyboards.inline.admin_panel.control_newsletter.main import control_newsletter_markup
from bot.fsm.newsletter import Newsletter

new_newsletter_callback_router = Router()


@new_newsletter_callback_router.callback_query(StateFilter(Newsletter.new_newsletter), F.data == 'back')
async def back_control_newsletter(query: CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=control_newsletter_markup.get_markup())
    await state.set_state(Newsletter.control_newsletter)
