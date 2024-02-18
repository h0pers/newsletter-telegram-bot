from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callback.categories import CategoriesAction
from bot.fsm.categories import Categories
from sqlalchemy import text
from bot.config import MessageText
from bot.database.main import tasks_db_session_local
from bot.callback.categories import Category
from bot.keyboards.inline.main import Inline
from bot.fsm.newsletter import Newsletter
from bot.keyboards.inline.admin_panel.control_newsletter.control_categories.main import control_categories_markup

delete_categories_callback_router = Router()


@delete_categories_callback_router.callback_query(CategoriesAction.filter(F.delete_category == 1))
async def delete_categories(query: CallbackQuery, state: FSMContext):
    async with tasks_db_session_local.begin() as session:
        statement = 'SELECT (id, title) FROM bot_message_categories;'
        categories = await session.execute(statement=text(statement))
        categories = categories.scalars().all()

    builder = InlineKeyboardBuilder()

    for category in categories:
        builder.button(text=category[1], callback_data=Category(category_id=category[0],
                                                                name=category[1]).pack())

    if len(categories) == 0:
        await query.answer(text=MessageText.NO_AVAILABLE_CATEGORIES)
    elif len(categories) >= 2:
        builder.adjust(round(len(categories) / 2), round(len(categories) / 2))

    await state.set_state(Categories.delete_category)
    await query.message.answer(text=MessageText.WOULD_DELETE_CATEGORIES,
                               reply_markup=builder.as_markup())
    await query.message.answer(text=MessageText.WOULD_CANCEL,
                               reply_markup=Inline([[Inline.cancel_button]]).get_markup())
    await query.answer()


@delete_categories_callback_router.callback_query(StateFilter(Categories.delete_category), Category.filter())
async def delete_category(query: CallbackQuery, callback_data: Category):
    async with tasks_db_session_local.begin() as session:
        statement = f'DELETE FROM bot_message_tasks WHERE category_id={callback_data.category_id}'
        await session.execute(statement=text(statement))
        statement = f'DELETE FROM bot_periodic_message_tasks WHERE category_id={callback_data.category_id}'
        await session.execute(statement=text(statement))
        statement = f'DELETE FROM bot_message_categories WHERE id={callback_data.category_id}'
        await session.execute(statement=text(statement))
        statement = 'SELECT (id, title) FROM bot_message_categories;'
        categories = await session.execute(statement=text(statement))
        categories = categories.scalars().all()

    builder = InlineKeyboardBuilder()
    for category in categories:
        builder.button(text=category[1], callback_data=Category(category_id=category[0],
                                                                name=category[1]).pack())
    if len(categories) == 0:
        await query.answer(text=MessageText.NO_AVAILABLE_CATEGORIES)
    elif len(categories) >= 2:
        builder.adjust(round(len(categories) / 2), round(len(categories) / 2))

    await query.message.edit_reply_markup(reply_markup=builder.as_markup())
    await query.answer(text=MessageText.CATEGORY_DELETED.format(category=callback_data.name))


@delete_categories_callback_router.callback_query(StateFilter(Categories.delete_category), F.data == 'cancel')
async def cancel_delete_categories(query: CallbackQuery, state: FSMContext):
    await state.set_state(Newsletter.control_newsletter)
    await query.message.answer(
        text=MessageText.ADMIN_PANEL.format(username=query.from_user.username or query.from_user.first_name),
        reply_markup=control_categories_markup.get_markup())
    await query.answer(text=MessageText.DONE)
