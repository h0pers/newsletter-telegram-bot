from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.sql import text

from bot.callback.newsletter import NewsletterAction
from bot.database.main import tasks_db_session_local
from bot.config import MessageText

publish_callback_router = Router()


@publish_callback_router.callback_query(NewsletterAction.filter(F.publish_newsletter == 1))
async def publish_newsletter(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data['message_thread_id']:
        data['message_thread_id'] = f"'{data['message_thread_id']}'"

    async with tasks_db_session_local.begin() as session:
        statement = f"SELECT id FROM channels WHERE chat_id={data['reply_chat_id']}"
        reply_chat = await session.execute(statement=text(statement))
        reply_chat = reply_chat.scalar()
        statement = f"""
INSERT INTO bot_message_tasks (message_id, from_chat_id, publish_time, message_thread_id, reply_chat_id) 
VALUES ('{data['message_id']}', '{data['from_chat_id']}', 
'{datetime.strptime(data['publish_time'], '%H:%M')}',{data['message_thread_id'] or 'NULL'}, '{reply_chat}');
"""
        await session.execute(statement=text(statement))

    await state.set_data({})
    await query.message.answer(text=MessageText.NEWSLETTER_PUBLISHED)
    await query.answer(text=MessageText.DONE)
