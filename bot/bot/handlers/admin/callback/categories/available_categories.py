import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import text

from bot.callback.categories import CategoriesAction
from bot.database.main import tasks_db_session_local
from bot.callback.categories import Category
from bot.config import MessageText

available_categories_callback_router = Router()


@available_categories_callback_router.callback_query(CategoriesAction.filter(F.available_category == 1))
async def available_categories(query: CallbackQuery, state: FSMContext):
    try:
        async with tasks_db_session_local.begin() as session:
            statement = 'SELECT (id, title) FROM bot_message_categories;'
            categories = await session.execute(statement=text(statement))
            categories = categories.scalars().all()
            logging.info(categories)

        builder = InlineKeyboardBuilder()
        for i in range(len(categories)):
            builder.button(text=categories[i][1], callback_data=Category(category_id=categories[i][0],
                                                                         name=categories[i][1]).pack())

        builder.adjust(round(len(categories) / 2), round(len(categories) / 2))
        await query.message.answer(text=MessageText.AVAILABLE_CATEGORIES, reply_markup=builder.as_markup())
        await query.answer()

    except Exception as exception:
        logging.exception(exception)


@available_categories_callback_router.callback_query(Category.filter())
async def category_detail(query: CallbackQuery, callback_data: Category, state: FSMContext):
    async with tasks_db_session_local.begin() as session:
        statement = f'SELECT id FROM bot_message_tasks WHERE category_id={callback_data.category_id};'
        category = await session.execute(statement=text(statement))
        category_rows = category.scalars().all()

    await query.answer(text=str(len(category_rows)))
