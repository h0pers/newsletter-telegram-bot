import telebot

from sqlalchemy import select
from datetime import datetime

from app.celery import app, logger
from app.config import BOT_TOKEN
from app.database.main import SessionLocal
from app.database.models.tasks import BotMessageTasks
from app.database.models.channels import Channels
from app.config import ADMINS_ID
from app.config import MessageText
from app.config import TIME_ZONE


@app.task(bind=True)
def check_forward_schedule(self):
    bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')
    with SessionLocal.begin() as session:
        tasks = session.scalars(select(BotMessageTasks)).all()

    for task in tasks:
        try:
            time_now = datetime.now(tz=TIME_ZONE).time()
            time_now = time_now.replace(second=0, microsecond=0)
            task_publish_time = task.publish_time.replace(second=0, microsecond=0)

            if task_publish_time == time_now:
                with SessionLocal.begin() as session:
                    reply_chat = session.scalars(select(Channels).filter_by(id=task.reply_chat_id)).one()

                bot.forward_message(chat_id=reply_chat.chat_id, message_id=task.message_id,
                                    message_thread_id=task.message_thread_id, from_chat_id=task.from_chat_id)
        except Exception as error:
            for admin_id in ADMINS_ID:
                bot.send_message(chat_id=admin_id,
                                 text=MessageText.SEND_MESSAGE_ERROR.format(error=error))
