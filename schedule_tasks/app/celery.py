from celery import Celery
from celery.schedules import crontab

from celery.utils.log import get_task_logger

from app.config import REDIS_URL, TIME_ZONE_STR, TASK_LIST

app = Celery('bot_celery', broker=REDIS_URL)
app.autodiscover_tasks(TASK_LIST)
app.conf.timezone = TIME_ZONE_STR
logger = get_task_logger(__name__)

app.conf.beat_schedule = {
    'Check static time message': {
        'task': 'app.tasks.static_time_message.tasks.check_static_time_message',
        'schedule': crontab(),
    },
    'Check periodic time message': {
        'task': 'app.tasks.periodic_time_message.tasks.check_periodic_time_message',
        'schedule': crontab(),
    },
}


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(), check_static_time_message.s(), name='Check static time message')
    sender.add_periodic_task(crontab(), check_periodic_time_message.s(), name='Check periodic time message')
