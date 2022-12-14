from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# установить модуль насторек Django по умолчанию для программы "Celery"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docker.settings')
app = Celery('docker')
# Использование строки здесь означает, что паботнику не нужно будет мариновать обьект при использовании Windows
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'trade': {
        'task': 'docker_admin.tasks.price',
        'schedule': crontab(),
    },

}


app.conf.beat_schedule = {
    'trade': {
        'task': 'docker_admin.tasks.trade',
        'schedule': crontab(),
    },

}