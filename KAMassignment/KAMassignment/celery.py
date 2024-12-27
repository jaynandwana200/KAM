from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KAMassignment.settings')

app = Celery("KAMassignment")

app.config_from_object(settings, namespace='CELERY')


# Celery Beat Settings

app.conf.beat_schedule = {

    'check_and_generate_new_interaction' : {
        'task' : 'KAM.tasks.generateInteractions',
        'schedule' : crontab(hour=16,minute=18), #time of day when task will run Automatically ( UTC )
    }
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')