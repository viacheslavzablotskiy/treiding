from __future__ import absolute_import, unicode_literals

from time import sleep
from .models import Offer
from celery import shared_task, Celery
from celery.schedules import crontab


@shared_task(run_every=(crontab(minute=1)))
def matrix(a,b):
    return a + b
# def trade():
#     try:
#         if Offer.objects.get(choices="BUY") or Offer.objects.get(choices="ADD"):
#             print("hello")
#     except:
#         raise ValueError("Данного офера нету ")
