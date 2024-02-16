from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callback.categories import CategoriesAction
from bot.fsm.categories import Categories

from bot.keyboards.inline.admin_panel.control_newsletter.control_categories.main import control_categories_markup
from bot.fsm.newsletter import Newsletter
from bot.keyboards.inline.admin_panel.control_newsletter.main import control_newsletter_markup

control_categories_callback_router = Router()


@control_categories_callback_router.callback_query(CategoriesAction.filter(F.control_categories == 1))
async def control_categories(query: CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=control_categories_markup.get_markup())
    await state.set_state(Categories.control_categories)


@control_categories_callback_router.callback_query(StateFilter(Categories.control_categories), F.data == 'back')
async def back_control_newsletter(query: CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=control_newsletter_markup.get_markup())
    await state.set_state(Newsletter.control_newsletter)
