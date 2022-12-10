from __future__ import absolute_import
# гарантия на то что приложение будет пользоваться этими услугами
from .celery import app as celery_app


__al__ = ('celery_app', )