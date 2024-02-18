import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import text

from bot.callback.categories import CategoriesAction
from bot.database.main import tasks_db_session_local
from bot.callback.categories import Category
from bot.config import MessageText
from bot.fsm.categories import Categories
from bot.keyboards.inline.main import Inline
from bot.keyboards.inline.admin_panel.control_newsletter.control_categories.main import control_categories_markup

available_categories_callback_router = Router()


@available_categories_callback_router.callback_query(CategoriesAction.filter(F.available_category == 1))
async def available_categories(query: CallbackQuery, state: FSMContext):
    try:
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
        await state.set_state(Categories.available_categories)
        await query.message.answer(text=MessageText.AVAILABLE_CATEGORIES, reply_markup=builder.as_markup())
        await query.message.answer(text=MessageText.WOULD_CANCEL,
                                   reply_markup=Inline([[Inline.cancel_button]]).get_markup())
        await query.answer()

    except ValueError:
        pass

    except Exception as exception:
        logging.exception(exception)


@available_categories_callback_router.callback_query(StateFilter(Categories.available_categories), Category.filter())
async def category_detail(query: CallbackQuery, callback_data: Category, state: FSMContext):
    async with tasks_db_session_local.begin() as session:
        statement = f'SELECT id FROM bot_message_tasks WHERE category_id={callback_data.category_id};'
        static_tasks = await session.execute(statement=text(statement))
        static_tasks = static_tasks.scalars().all()
        statement = f'SELECT id FROM bot_periodic_message_tasks WHERE category_id={callback_data.category_id};'
        periodic_tasks = await session.execute(statement=text(statement))
        periodic_tasks = periodic_tasks.scalars().all()

    await query.message.answer(text=MessageText.CATEGORY_DETAILS.format(category=callback_data.name,
                                                                        static_tasks=len(static_tasks),
                                                                        periodic_tasks=len(periodic_tasks)))
    await query.answer()


@available_categories_callback_router.callback_query(StateFilter(Categories.available_categories), F.data == 'cancel')
async def cancel_available_categories(query: CallbackQuery, state: FSMContext):
    await state.set_state(Categories.control_categories)
    await query.message.answer(text=MessageText.ADMIN_PANEL.format(username=query.from_user.username or query.from_user.first_name),
                               reply_markup=control_categories_markup.get_markup())
    await query.answer(text=MessageText.DONE)
