import random
import telebot
import datetime

from sqlalchemy import select, text

from app.celery import app, logger
from app.config import BOT_TOKEN, MIN_SEND_MESSAGE_DELAY, MAX_SEND_MESSAGE_DELAY
from app.database.main import SessionLocal
from app.database.models.channels import Channels
from app.config import ADMINS_ID
from app.config import MessageText
from app.config import TIME_ZONE
from app.database.models.tasks import BotPeriodicMessageTasks


@app.task()
def send_periodic_time_message(task):
    bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')
    try:
        with SessionLocal.begin() as session:
            statement = f'UPDATE bot_periodic_message_tasks SET last_publish_time=NOW() WHERE id={task["id"]};'
            session.execute(statement=text(statement))
            reply_chat = session.scalars(select(Channels).filter_by(id=task['reply_chat_id'])).one()

        bot.forward_message(chat_id=reply_chat.chat_id, message_id=task['message_id'],
                            message_thread_id=task['message_thread_id'], from_chat_id=task['from_chat_id'])
    except Exception as error:
        for admin_id in ADMINS_ID:
            bot.send_message(chat_id=admin_id,
                             text=MessageText.SEND_MESSAGE_ERROR.format(error=error))


@app.task(bind=True)
def check_periodic_time_message(self):
    with SessionLocal.begin() as session:
        tasks = session.scalars(select(BotPeriodicMessageTasks)).all()

    for task in tasks:
        time_now = datetime.datetime.now(tz=TIME_ZONE).now()
        time_now = time_now.replace(second=0, microsecond=0)
        last_publish_time = task.last_publish_time.replace(second=0, microsecond=0)
        if time_now == last_publish_time + task.time_interval:
            task_kwargs = {
                'id': task.id,
                'reply_chat_id': task.reply_chat_id,
                'message_id': task.message_id,
                'message_thread_id': task.message_thread_id,
                'from_chat_id': task.from_chat_id
            }
            time_now = datetime.datetime.now(tz=TIME_ZONE)
            time_delay = datetime.timedelta(hours=0,
                                            minutes=random.randrange(MIN_SEND_MESSAGE_DELAY, MAX_SEND_MESSAGE_DELAY),
                                            seconds=0)
            send_periodic_time_message.apply_async(args=[task_kwargs], eta=time_now + time_delay)
