import logging
from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.sql import text

from bot.callback.newsletter import NewsletterAction
from bot.database.main import tasks_db_session_local
from bot.config import MessageText
from bot.fsm.newsletter import Newsletter

publish_callback_router = Router()


@publish_callback_router.callback_query(NewsletterAction.filter(F.publish_newsletter == 1))
async def publish_newsletter(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if data.get('message_thread_id') is not None:
        data['message_thread_id'] = f"'{data['message_thread_id']}'"

    if data.get('period_time_data') is not None:
        time_data = data['period_time_data']
        async with tasks_db_session_local.begin() as session:
            for reply_chat_id in data['reply_chats_id']:
                statement = f"""
INSERT INTO bot_periodic_message_tasks (message_id, from_chat_id, time_interval, message_thread_id, reply_chat_id) 
VALUES ('{data['message_id']}', '{data['from_chat_id']}', 
'{timedelta(days=time_data[0], hours=time_data[1], minutes=time_data[2])}', {data['message_thread_id'] or 'NULL'}, 
'{reply_chat_id}');
"""
                await session.execute(statement=text(statement))

    elif data['publish_time']:
        async with tasks_db_session_local.begin() as session:
            for reply_chat_id in data['reply_chats_id']:
                statement = f"""
INSERT INTO bot_message_tasks (message_id, from_chat_id, publish_time, message_thread_id, reply_chat_id) 
VALUES ('{data['message_id']}', '{data['from_chat_id']}', 
'{datetime.strptime(data['publish_time'], '%H:%M')}',{data['message_thread_id'] or 'NULL'}, 
'{reply_chat_id}');
"""
                await session.execute(statement=text(statement))

    await state.set_state(Newsletter.new_newsletter)
    await state.set_data({})
    await query.message.answer(text=MessageText.NEWSLETTER_PUBLISHED)
    await query.answer(text=MessageText.DONE)

