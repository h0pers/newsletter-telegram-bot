import os

import pytz
from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

BOT_TOKEN = os.getenv('BOT_TOKEN')

REDIS_URL = f'redis://{os.getenv("REDIS_HOST")}:{os.getenv("REDIS_PORT")}/0'

TIME_ZONE_STR = os.getenv('TZ')

ADMINS_ID = [int(admin.strip()) for admin in os.getenv('TELEGRAM_ADMIN_ID').split(',')]

TIME_ZONE = pytz.timezone(TIME_ZONE_STR)

TASK_LIST = [
    'app.tasks.static_time_message',
    'app.tasks.periodic_time_message',
]

DB_URL = conn_url = f'postgresql+psycopg://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}/{os.getenv("POSTGRES_DB")}'


class MessageText:
    SEND_MESSAGE_ERROR = '''
<b>Произошла ошибка при отправлении сообщение.</b>
Если вы недавно добавляли канал или рассылку проверьте что бот состоит в этом канале и имеет права администратора
<b>Код и описание ошибки:</b>
<code>{error}</code>
<b>Напишите сюда для бесплатной консультации
@dhryshchenkowork</b>
'''
