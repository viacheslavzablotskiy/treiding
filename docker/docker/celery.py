from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docker.settings')
app = Celery('docker')
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()


