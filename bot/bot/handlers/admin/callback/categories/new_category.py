from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callback.categories import CategoriesAction
from bot.fsm.categories import Categories
from bot.config import MessageText
from bot.keyboards.inline.main import Inline
from bot.keyboards.inline.admin_panel.control_newsletter.control_categories.main import control_categories_markup

new_category_callback_router = Router()


@new_category_callback_router.callback_query(CategoriesAction.filter(F.new_category == 1))
async def new_category(query: CallbackQuery, state: FSMContext):
    await query.message.answer(text=MessageText.NEW_CATEGORY,
                               reply_markup=Inline([[Inline.cancel_button]]).get_markup())
    await state.set_state(Categories.new_category)
    await query.answer()


@new_category_callback_router.callback_query(StateFilter(Categories.new_category), F.data == 'cancel')
async def cancel(query: CallbackQuery, state: FSMContext):
    await query.message.answer(
        text=MessageText.ADMIN_PANEL.format(username=query.message.from_user.username or query.message.from_user.first_name),
        reply_markup=control_categories_markup.get_markup())
    await state.set_state(Categories.control_categories)
    await query.answer(text=MessageText.CANCELED)

