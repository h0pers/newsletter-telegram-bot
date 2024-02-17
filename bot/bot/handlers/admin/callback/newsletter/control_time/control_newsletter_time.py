import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callback.newsletter import NewsletterAction
from bot.fsm.newsletter import Newsletter
from bot.keyboards.inline.admin_panel.control_newsletter.new_newsletter.control_time import control_time_markup
from bot.keyboards.inline.admin_panel.control_newsletter.new_newsletter.main import new_newsletter_markup

control_newsletter_time_callback_router = Router()


@control_newsletter_time_callback_router.callback_query(NewsletterAction.filter(F.control_newsletter_time == 1))
async def control_time(query: CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=control_time_markup.get_markup())
    logging.info(await state.get_data())
    await state.set_state(Newsletter.control_newsletter_time)


@control_newsletter_time_callback_router.callback_query(StateFilter(Newsletter.control_newsletter_time), F.data == 'back')
async def back_new_newsletter(query: CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=new_newsletter_markup.get_markup())
    await state.set_state(Newsletter.new_newsletter)
