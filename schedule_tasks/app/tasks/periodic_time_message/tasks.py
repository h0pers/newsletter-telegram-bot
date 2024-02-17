import logging

import telebot

from sqlalchemy import select, text
from datetime import datetime

from app.celery import app, logger
from app.config import BOT_TOKEN
from app.database.main import SessionLocal
from app.database.models.channels import Channels
from app.config import ADMINS_ID
from app.config import MessageText
from app.config import TIME_ZONE
from app.database.models.tasks import BotPeriodicMessageTasks


@app.task(bind=True)
def check_periodic_time_message(self):
    bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')
    with SessionLocal.begin() as session:
        tasks = session.scalars(select(BotPeriodicMessageTasks)).all()

    for task in tasks:
        try:
            time_now = datetime.now(tz=TIME_ZONE).now()
            time_now = time_now.replace(second=0, microsecond=0)
            last_publish_time = task.last_publish_time.replace(second=0, microsecond=0)

            if time_now == last_publish_time + task.time_interval:
                with SessionLocal.begin() as session:
                    statement = f'UPDATE bot_periodic_message_tasks SET last_publish_time=NOW() WHERE id={task.id};'
                    logging.info(statement)
                    session.execute(statement=text(statement))
                    reply_chat = session.scalars(select(Channels).filter_by(id=task.reply_chat_id)).one()

                bot.forward_message(chat_id=reply_chat.chat_id, message_id=task.message_id,
                                    message_thread_id=task.message_thread_id, from_chat_id=task.from_chat_id)
        except Exception as error:
            for admin_id in ADMINS_ID:
                bot.send_message(chat_id=admin_id,
                                 text=MessageText.SEND_MESSAGE_ERROR.format(error=error))
