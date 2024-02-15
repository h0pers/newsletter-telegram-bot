from celery import Celery
from celery.schedules import crontab

from celery.utils.log import get_task_logger

from app.config import REDIS_URL, TIME_ZONE_STR, TASK_LIST

app = Celery('bot_celery', broker=REDIS_URL)
app.autodiscover_tasks(TASK_LIST)
app.conf.timezone = TIME_ZONE_STR
logger = get_task_logger(__name__)

app.conf.beat_schedule = {
    'Check forward schedule': {
        'task': 'app.tasks.forward_message.tasks.check_forward_schedule',
        'schedule': crontab(),
    },
}


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(), check_forward_schedule.s(), name='Check forward schedule')
