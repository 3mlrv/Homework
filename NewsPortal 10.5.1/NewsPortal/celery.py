import os
from celery import Celery
from celery.schedules import crontab

 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')
 
app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace = 'CELERY')


app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'news.tasks.send_weekly_mail',
        'schedule': crontab(minute='21', hour='14', day_of_week='thursday'),
    },
}

app.conf.timezone = 'UTC'
app.autodiscover_tasks()