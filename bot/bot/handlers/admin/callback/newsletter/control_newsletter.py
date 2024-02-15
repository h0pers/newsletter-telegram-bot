from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from bot.callback.newsletter import NewsletterAction
from bot.keyboards.inline.admin_panel.control_newsletter.main import control_newsletter_markup
from bot.keyboards.inline.admin_panel.main import admin_panel_markup
from bot.fsm.newsletter import Newsletter
from bot.keyboards.inline.admin_panel.control_newsletter.new_newsletter.main import new_newsletter_markup
from bot.keyboards.inline.main import Inline
from bot.config import MessageText

control_newsletter_callback_router = Router()


@control_newsletter_callback_router.callback_query(NewsletterAction.filter(F.control_newsletter == 1))
async def control_newsletter(query: CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=control_newsletter_markup.get_markup())
    await state.set_state(Newsletter.control_newsletter)


@control_newsletter_callback_router.callback_query(NewsletterAction.filter(F.new_newsletter == 1))
async def new_newsletter(query: CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=new_newsletter_markup.get_markup())
    await state.set_state(Newsletter.new_newsletter)


@control_newsletter_callback_router.callback_query(StateFilter(Newsletter.control_newsletter), F.data == 'back')
async def back_admin_panel(query: CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=admin_panel_markup.get_markup())
    await state.clear()
