import logging

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import text

from bot.callback.newsletter import NewsletterTypes
from bot.fsm.newsletter import Newsletter
from bot.config import MessageText
from bot.database.main import tasks_db_session_local
from bot.keyboards.inline.main import Inline
from bot.keyboards.inline.admin_panel.control_newsletter.available_newsletters.main import choose_newsletter_type
from bot.callback.newsletter import NewsletterAction
from bot.keyboards.inline.main import InlineButtonText
from bot.callback.categories import Category

periodic_newsletter_callback_router = Router()


@periodic_newsletter_callback_router.callback_query(NewsletterTypes.filter(F.periodic_message == 1))
async def choose_category(query: CallbackQuery, state: FSMContext):
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
        await state.set_state(Newsletter.edit_periodic_newsletter)
        await query.message.answer(text=MessageText.AVAILABLE_CATEGORIES, reply_markup=builder.as_markup())
        await query.answer()

    except ValueError:
        pass

    except Exception as exception:
        logging.exception(exception)


@periodic_newsletter_callback_router.callback_query(StateFilter(Newsletter.edit_periodic_newsletter),
                                                    Category.filter())
async def periodic_newsletter(query: CallbackQuery, callback_data: Category, bot: Bot, state: FSMContext):
    async with tasks_db_session_local.begin() as session:
        statement = f'''
        SELECT (id, message_id) 
        FROM bot_periodic_message_tasks WHERE category_id={callback_data.category_id};
        '''

        tasks = await session.execute(statement=text(statement))
        tasks = tasks.scalars().all()
        try:
            messages_id = set([tasks[i][1] for i in range(len(tasks))])
            logging.info(messages_id)
        except:
            logging.info('No periodic newsletters')

        for message_id in messages_id:
            statement = f'''
            SELECT (id, reply_chat_id, from_chat_id, message_id, message_thread_id, time_interval) 
            FROM bot_periodic_message_tasks WHERE message_id='{message_id}';
            '''
            tasks = await session.execute(statement=text(statement))
            tasks = tasks.scalars().all()
            statement = f'''
SELECT chat_username FROM channels WHERE id IN
({", ".join(str(tasks[i][1]) for i in range(len(tasks)))});'''
            channel = await session.execute(statement=text(statement))
            channel_usernames = channel.scalars().all()
            delete_button = InlineKeyboardButton(text=InlineButtonText.DELETE_BUTTON,
                                                 callback_data=NewsletterAction(newsletter_message_id=message_id,
                                                                                delete_newsletter=1).pack())
            await query.message.answer(
                text=MessageText.PERIODIC_NEWSLETTER_DETAILS.format(username=' @'.join(channel_usernames),
                                                                    publish_time=tasks[0][5]),
                reply_markup=Inline([[delete_button]]).get_markup())
            await bot.forward_message(chat_id=query.message.chat.id, from_chat_id=tasks[0][2], message_id=tasks[0][3],
                                      message_thread_id=tasks[0][4])

        await query.message.answer(text=MessageText.WOULD_CANCEL,
                                   reply_markup=Inline([[Inline.cancel_button]]).get_markup())
    await query.answer()


@periodic_newsletter_callback_router.callback_query(StateFilter(Newsletter.edit_periodic_newsletter),
                                                    NewsletterAction.filter(
                                                        F.delete_newsletter == 1 and F.newsletter_message_id != 0))
async def delete_periodic_newsletter(query: CallbackQuery, callback_data: NewsletterAction):
    async with tasks_db_session_local.begin() as session:
        statement = f'DELETE FROM bot_periodic_message_tasks WHERE message_id={callback_data.newsletter_message_id}'
        await session.execute(statement=text(statement))

    await query.message.edit_text(text=query.message.text + '\n<b>Удалено.</b>')
    await query.answer(text=MessageText.DONE)


@periodic_newsletter_callback_router.callback_query(StateFilter(Newsletter.edit_periodic_newsletter),
                                                    F.data == 'cancel')
async def cancel_periodic_newsletter(query: CallbackQuery, state: FSMContext):
    await state.set_state(Newsletter.edit_newsletter)
    await query.message.answer(
        text=MessageText.ADMIN_PANEL.format(username=query.from_user.username or query.from_user.first_name),
        reply_markup=choose_newsletter_type.get_markup())
    await query.answer()
