from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from docker_admin.models import Offer, Balance, User
from django.db.models import signals
from docker_admin.tasks import create_offer, send_verification_email
from .tasks import Trading


@transaction.atomic
@receiver(post_save, sender=Offer)
def create_offer_(sender, instance, created, signal, *args, **kwargs):
    if created:
        create_offer.delay()


@transaction.atomic
@receiver(post_save, sender=User)
def register_account(sender, instance, created, signal, *args, **kwargs):
    if not instance.is_verified:
        send_verification_email.delay(instance.pk)


@receiver(post_save, sender=Offer)
def make_trade(sender, instance, created, signal, *args, **kwargs):
    if created:
        Trading.find_suitable_sell_offer_and_make_trade()
