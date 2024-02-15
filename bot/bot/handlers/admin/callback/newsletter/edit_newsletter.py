import datetime
import logging

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton
from sqlalchemy.sql import text

from bot.config import MessageText
from bot.callback.newsletter import NewsletterAction
from bot.database.main import tasks_db_session_local
from bot.fsm.newsletter import Newsletter
from bot.keyboards.inline.main import Inline
from bot.keyboards.inline.main import InlineButtonText
from bot.keyboards.inline.admin_panel.main import admin_panel_markup

edit_newsletter_callback_router = Router()


@edit_newsletter_callback_router.callback_query(NewsletterAction.filter(F.edit_newsletter == 1))
async def edit_newsletter(query: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(Newsletter.edit_newsletter)
    await query.message.answer(text=MessageText.AVAILABLE_NEWSLETTER)
    async with tasks_db_session_local.begin() as session:
        statement = 'SELECT * FROM bot_message_tasks;'
        newsletters = await session.execute(statement=text(statement))

    for newsletter in newsletters:
        async with tasks_db_session_local.begin() as session:
            statement = f'SELECT (chat_username, creation_date) FROM channels WHERE id={newsletter.reply_chat_id};'
            channel = await session.execute(statement=text(statement))
            channel = channel.scalars().all()
            chat_username = channel[0][0]
            creation_date = channel[0][1]

        delete_button = InlineKeyboardButton(text=InlineButtonText.DELETE_BUTTON,
                                             callback_data=NewsletterAction(delete_newsletter=newsletter.id).pack())
        await query.message.answer(text=MessageText.NEWSLETTER_DETAILS.format(username=chat_username,
                                                                              creation_date=creation_date.strftime(
                                                                                  '%m/%d/%Y'),
                                                                              publish_time=newsletter.publish_time.strftime(
                                                                                  '%H:%M')),
                                   reply_markup=Inline([[delete_button]]).get_markup())

        await bot.forward_message(chat_id=query.message.chat.id, message_id=newsletter.message_id,
                                  message_thread_id=newsletter.message_thread_id, from_chat_id=newsletter.from_chat_id)

    await query.message.answer(text=MessageText.WOULD_CANCEL,
                               reply_markup=Inline([[Inline.cancel_button]]).get_markup())
    await query.answer()


@edit_newsletter_callback_router.callback_query(StateFilter(Newsletter.edit_newsletter), NewsletterAction.filter(F.delete_newsletter != 0))
async def delete_newsletter(query: CallbackQuery, callback_data: NewsletterAction, state: FSMContext):
    async with tasks_db_session_local.begin() as session:
        statement = f'DELETE FROM bot_message_tasks WHERE id={callback_data.delete_newsletter}'
        await session.execute(statement=text(statement))

    await query.message.edit_text(text=f'{query.message.text}\n<b>Удалено.</b>')
    await query.answer(text=MessageText.DONE)


@edit_newsletter_callback_router.callback_query(StateFilter(Newsletter.edit_newsletter), F.data == 'cancel')
async def cancel_edit_newsletter(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.answer(
        text=MessageText.ADMIN_PANEL.format(username=query.from_user.username or query.from_user.first_name),
        reply_markup=admin_panel_markup.get_markup())
    await query.answer()
