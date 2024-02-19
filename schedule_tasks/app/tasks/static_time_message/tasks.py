import logging
import random
import datetime
import telebot

from sqlalchemy import text

from app.celery import app, logger
from app.config import BOT_TOKEN
from app.config import PUBLISH_PER_REQUEST
from app.database.main import SessionLocal
from app.config import ADMINS_ID
from app.config import MessageText
from app.config import TIME_ZONE
from app.config import MIN_SEND_MESSAGE_DELAY, MAX_SEND_MESSAGE_DELAY


@app.task()
def send_static_time_message(task):
    bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')
    datetime_now = datetime.datetime.now(tz=TIME_ZONE)
    date_now = datetime_now.date()
    try:
        with SessionLocal.begin() as session:
            statement = f'''
        SELECT id FROM bot_message_tasks WHERE last_publish_date >= '{date_now - datetime.timedelta(days=1)}';
        '''
            tasks_published = session.execute(statement=text(statement)).scalars().all()
            if len(tasks_published) >= PUBLISH_PER_REQUEST:
                logging.info('Publish limit is over per day')
                return
            statement = f"UPDATE bot_message_tasks SET last_publish_date=NOW() WHERE id={task['id']};"
            session.execute(statement=text(statement))
            statement = f"SELECT chat_id FROM channels WHERE id={task['reply_chat_id']};"
            reply_chat = session.execute(text(statement))
            reply_chat_id = reply_chat.scalar()

        bot.forward_message(chat_id=reply_chat_id, message_id=task['message_id'],
                            message_thread_id=task['message_thread_id'], from_chat_id=task['from_chat_id'])
    except Exception as error:
        for admin_id in ADMINS_ID:
            bot.send_message(chat_id=admin_id,
                             text=MessageText.SEND_MESSAGE_ERROR.format(error=error))


@app.task(bind=True)
def check_static_time_message(self):
    datetime_now = datetime.datetime.now(tz=TIME_ZONE)
    with SessionLocal.begin() as session:
        date_now = datetime_now.date()
        statement = f'''
SELECT (id, reply_chat_id, message_id, message_thread_id, from_chat_id, publish_time, last_publish_date) 
FROM bot_message_tasks
WHERE last_publish_date <= '{date_now - datetime.timedelta(days=1)}' OR last_publish_date IS NULL 
ORDER BY last_publish_date;
'''
        tasks = session.scalars(statement=text(statement)).all()
    for task in tasks:
        time_now = datetime.datetime.now(tz=TIME_ZONE).time()
        time_now = time_now.replace(second=0, microsecond=0)
        task_publish_date = datetime.datetime.strptime(task[5], '%H:%M:%S').replace(second=0, microsecond=0)

        if task_publish_date.time() == time_now:
            task_kwargs = {
                'id': task[0],
                'reply_chat_id': task[1],
                'message_id': task[2],
                'message_thread_id': task[3],
                'from_chat_id': task[4]
            }
            time_now = datetime.datetime.now(tz=TIME_ZONE)
            time_delay = datetime.timedelta(minutes=0, seconds=random.uniform(MIN_SEND_MESSAGE_DELAY, MAX_SEND_MESSAGE_DELAY), microseconds=0)
            send_static_time_message.apply_async(args=[task_kwargs], eta=time_now + time_delay)
