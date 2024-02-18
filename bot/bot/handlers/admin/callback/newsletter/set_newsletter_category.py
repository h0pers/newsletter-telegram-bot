import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import text

from bot.callback.newsletter import NewsletterAction
from bot.callback.categories import Category
from bot.config import MessageText
from bot.database.main import tasks_db_session_local
from bot.fsm.newsletter import Newsletter
from bot.keyboards.inline.main import Inline

from bot.keyboards.inline.admin_panel.control_newsletter.new_newsletter.main import new_newsletter_markup

set_newsletter_category_callback_router = Router()


@set_newsletter_category_callback_router.callback_query(NewsletterAction.filter(F.set_newsletter_category == 1))
async def set_category(query: CallbackQuery, state: FSMContext):
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
        await state.set_state(Newsletter.set_newsletter_category)
        await query.message.answer(text=MessageText.AVAILABLE_CATEGORIES, reply_markup=builder.as_markup())
        await query.message.answer(text=MessageText.WOULD_CANCEL,
                                   reply_markup=Inline([[Inline.cancel_button]]).get_markup())
        await query.answer()

    except ValueError:
        pass

    except Exception as exception:
        logging.exception(exception)


@set_newsletter_category_callback_router.callback_query(StateFilter(Newsletter.set_newsletter_category),
                                                        Category.filter())
async def choose_category(query: CallbackQuery, callback_data: Category, state: FSMContext):
    await state.set_state(Newsletter.new_newsletter)
    await state.update_data({'category_id': callback_data.category_id})
    await query.message.answer(text=MessageText.CHOSEN_CATEGORY.format(category=callback_data.name))
    await query.message.answer(
        text=MessageText.ADMIN_PANEL.format(username=query.from_user.username or query.from_user.first_name),
        reply_markup=new_newsletter_markup.get_markup())
    await query.answer(text=MessageText.DONE)


@set_newsletter_category_callback_router.callback_query(StateFilter(Newsletter.set_newsletter_category),
                                                        F.data == 'cancel')
async def cancel_set_category(query: CallbackQuery, state: FSMContext):
    await state.set_state(Newsletter.new_newsletter)
    await query.message.answer(
        text=MessageText.ADMIN_PANEL.format(username=query.from_user.username or query.from_user.first_name),
        reply_markup=new_newsletter_markup.get_markup())
    await query.answer(text=MessageText.DONE)
