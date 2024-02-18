import logging

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import text

from bot.fsm.newsletter import Newsletter
from bot.callback.newsletter import NewsletterTypes, NewsletterAction
from bot.config import MessageText
from bot.database.main import tasks_db_session_local
from bot.keyboards.inline.main import Inline, InlineButtonText
from bot.keyboards.inline.admin_panel.control_newsletter.available_newsletters.main import choose_newsletter_type
from bot.callback.categories import Category
from bot.filters.has_states import HasStates

static_newsletter_callback_router = Router()


@static_newsletter_callback_router.callback_query(NewsletterTypes.filter(F.static_message == 1))
async def static_newsletter_categories(query: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        async with tasks_db_session_local.begin() as session:
            statement = 'SELECT category_id FROM bot_message_tasks;'
            categories_id = await session.execute(statement=text(statement))
            categories_id = categories_id.scalars().all()
            builder = InlineKeyboardBuilder()
            for i in range(len(categories_id)):
                statement = f'SELECT title FROM bot_message_categories WHERE id={categories_id[i]};'
                category = await session.execute(statement=text(statement))
                category_name = category.scalar()
                builder.button(text=category_name, callback_data=Category(category_id=categories_id[i],
                                                                          name=category_name).pack())

            if len(categories_id) == 0:
                await query.answer(text=MessageText.NO_AVAILABLE_TASKS)
                return
            elif len(categories_id) >= 2:
                builder.adjust(round(len(categories_id) / 2), round(len(categories_id) / 2))

        await state.set_state(Newsletter.choose_static_newsletter_category)
        await query.message.answer(text=MessageText.AVAILABLE_CATEGORIES, reply_markup=builder.as_markup())
        await query.message.answer(text=MessageText.WOULD_CANCEL,
                                   reply_markup=Inline([[Inline.cancel_button]]).get_markup())
        await query.answer()

    except ValueError:
        pass

    except Exception as exception:
        logging.exception(exception)


@static_newsletter_callback_router.callback_query(StateFilter(Newsletter.choose_static_newsletter_category),
                                                  Category.filter())
async def static_newsletter(query: CallbackQuery, callback_data: Category, bot: Bot, state: FSMContext):
    async with tasks_db_session_local.begin() as session:
        statement = f'''
        SELECT (id, reply_chat_id, from_chat_id, message_id, message_thread_id, publish_time) 
        FROM bot_message_tasks WHERE category_id={callback_data.category_id};
        '''

        tasks = await session.execute(statement=text(statement))
        tasks = tasks.scalars().all()

        for task in tasks:
            statement = f'SELECT chat_username FROM channels WHERE id={task[1]};'
            channel = await session.execute(statement=text(statement))
            channel_username = channel.scalar()
            delete_button = InlineKeyboardButton(text=InlineButtonText.DELETE_BUTTON,
                                                 callback_data=NewsletterAction(newsletter_id=task[0],
                                                                                delete_newsletter=1).pack())
            await query.message.answer(text=MessageText.NEWSLETTER_DETAILS.format(username=channel_username,
                                                                                  publish_time=task[5]),
                                       reply_markup=Inline([[delete_button]]).get_markup())
            await bot.forward_message(chat_id=query.message.chat.id, from_chat_id=task[2], message_id=task[3],
                                      message_thread_id=task[4])

    await state.set_state(Newsletter.edit_static_newsletter)
    await query.answer()


@static_newsletter_callback_router.callback_query(StateFilter(Newsletter.edit_static_newsletter),
                                                  NewsletterAction.filter(
                                                      F.delete_newsletter == 1 and F.newsletter_id != 0))
async def delete_static_newsletter(query: CallbackQuery, callback_data: NewsletterAction):
    async with tasks_db_session_local.begin() as session:
        statement = f'DELETE FROM bot_message_tasks WHERE id={callback_data.newsletter_id}'
        await session.execute(statement=text(statement))

    await query.message.edit_text(text=query.message.text + '\n<b>Удалено.</b>')
    await query.answer(text=MessageText.DONE)


@static_newsletter_callback_router.callback_query(HasStates([Newsletter.choose_static_newsletter_category,
                                                             Newsletter.edit_static_newsletter]),
                                                  F.data == 'cancel')
async def cancel_static_newsletter(query: CallbackQuery, state: FSMContext):
    await state.set_state(Newsletter.edit_newsletter)
    await query.message.answer(text=MessageText.ADMIN_PANEL.format(username=query.from_user.username or query.from_user.first_name),
                               reply_markup=choose_newsletter_type.get_markup())
    await query.answer()

