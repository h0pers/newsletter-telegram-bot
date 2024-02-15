import os

import pytz
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

BOT_TOKEN = os.getenv('BOT_TOKEN')

DB_URL = f'postgresql+asyncpg://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}/{os.getenv("POSTGRES_DB")}'

SCHEDULE_DB_URL = f'postgresql+asyncpg://{os.getenv("SCHEDULE_POSTGRES_USER")}:{os.getenv("SCHEDULE_POSTGRES_PASSWORD")}@{os.getenv("SCHEDULE_POSTGRES_HOST")}/{os.getenv("SCHEDULE_POSTGRES_DB")}'

ADMINS_ID = [int(admin.strip()) for admin in os.getenv('TELEGRAM_ADMIN_ID').split(',')]

TIME_ZONE = pytz.timezone(os.getenv('TZ'))


class MessageText:
    NO_ADMIN_PERMISSION = '''<b>🚫 Вы не являетесь администратором этого телеграм бота 🚫</b> Уточните эту информацию у создателя.'''
    ADMIN_PANEL = '👋 Приветствуем вас <b>{username}</b> в панеле администратора! Что вам нужно сделать?'
    AVAILABLE_NEWSLETTER = 'Доступные рассылки:'
    ADD_CHANNEL = 'Перешлите сюда сообщение из канала куда должны отправляться сообщение.'
    ADD_MESSAGE = 'Перешлите или напишите сюда сообщение которое должно быть отправлено.'
    PICK_NEWSLETTER_CHAT = 'Напишите цифру чата который вам нужен.'
    ADD_CHANNEL_ERROR = 'Не возможно добавить канал. Убедитесь правильно ли вы отправили сообщение.'
    ADD_CHANNEL_SUCCESSFUL = 'Чат успешно добавлен.'
    CHANNEL_EXIST = 'Такой чат уже есть'
    WOULD_DELETE_CHANNEL = 'Выберете какой канал вы хотите удалить:'
    CHANNEL_DETAILS = '''
<b>Название чата:</b> @{username}
<b>Дата добавление:</b> {creation_date}
'''
    NEWSLETTER_DETAILS = '''
<b>Название чата:</b> @{username}
<b>Дата добавление:</b> {creation_date}
<b>Время публикации:</b> {publish_time}
    '''
    AVAILABLE_CHANNELS = 'Доступные каналы:'
    NO_AVAILABLE_CHANNELS = 'Нету доступных каналов'
    CHANNEL_NOT_FOUND = 'Чат не найден, попробуйте ещё раз'
    CHANNEL_PICKED = 'Чат успешно выбран.'
    CANCELED = 'Отменено'
    WOULD_CANCEL = 'Желаете отменить действие?'
    ERROR_MESSAGE = 'Произошла ошибка, убедитесь все ли правильно сделано. Попробуйте ещё раз.'
    MESSAGE_ADDED = 'Сообщение успешно добавлено.'
    SET_MESSAGE_TIME = 'Напишите время отправки сообщение. Формат: 13:15'
    SET_MESSAGE_SUCCESSFULUl = 'Время установлено.'
    SET_MESSAGE_TIME_ERROR = 'Не правильный формат времени. Попробуйте ещё раз.'
    DONE = 'Выполнено'
    NEWSLETTER_PUBLISHED = 'Сообщение опубликовано.'

