from __future__ import absolute_import, unicode_literals

import logging

from celery import shared_task
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import OutstandingToken
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework.authtoken.models import Token
from docker.celery import app
from docker_admin.models import Trade, Item, User, Balance, Inventory, Offer


@shared_task
def create_offer():
    offer_sell = list(Offer.objects.filter(type_function=2, is_activate=True))
    for offer in offer_sell:
        if not offer.is_activate:
            continue
        else:
            offer_buy_inventory = list(Inventory.objects.filter(user=offer.user))
            offer_buy_inventory.quantity = offer_buy_inventory.quantity - offer.quantity
            offer_buy_inventory.save()
            offer.save()
            # offer_buy_inventory = offer_buy_inventory[0]
            # if offer.quantity > offer_buy_inventory.quantity:
            #     offer.is_activate = False
            #     offer.save()
            # else:
            #     offer_buy_inventory.quantity = offer_buy_inventory.quantity - offer.quantity
            #     offer.is_locked = False
            #     offer_buy_inventory.save()
            #     offer.save()


@app.task
def send_verification_email(user_id):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
        token = list(OutstandingToken.objects.filter(user=user))
        token = token[0]
        send_mail(
            'Verify your QuickPublisher account',
            'Follow this link to verify your account: '
            'http://localhost:8000%s' % reverse('message', kwargs={'token': str(token.token)}),
            'zlava.mag@gmail.com',
            [user.email],
            fail_silently=False,
        )
    except UserModel.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)


@shared_task
def more_price():
    p = list(Trade.objects.all().order_by("price_total_1"))
    if p:
        p = p[-1]
        g = list(Item.objects.all())
        g = g[0]
        g.max_price = p.price_total_1
        g.save()
    else:
        print('не было не одной покупки')


class Trading:
    @classmethod
    def find_suitable_sell_offer_and_make_trade(cls):
        list_offer_for_buyer = list(Offer.objects.filter(type_function=1, is_activate=True))
        if list_offer_for_buyer:
            for offer_buy in list_offer_for_buyer:
                list_offer_seller = list(
                    Offer.objects.filter(type_function=2, is_activate=True, is_locked=False,
                                         price__gte=offer_buy.price))
                first_offer_seller = list_offer_seller[0]
                balance_offer_buy = list(Balance.objects.filter(user=offer_buy.user))
                balance_offer_buy = balance_offer_buy[0]
                balance_offer_sell = list(Balance.objects.filter(user=first_offer_seller.user))
                balance_offer_sell = balance_offer_sell[0]
                inventory_offer_buy = list(Inventory.objects.filter(user=offer_buy.user))
                inventory_offer_buy = inventory_offer_buy[0]
                inventory_offer_sell = list(Inventory.objects.filter(user=first_offer_seller.user))
                inventory_offer_sell = inventory_offer_sell[0]
                if first_offer_seller and balance_offer_buy.balance > first_offer_seller.total_price_is_offer:
                    cls._make_trade_(offer_buy=offer_buy, first_offer_seller=first_offer_seller,
                                     balance_offer_sell=balance_offer_sell, balance_offer_buy=balance_offer_buy,
                                     inventory_offer_buy=inventory_offer_buy, inventory_offer_sell=inventory_offer_sell)
                else:
                    continue

    @classmethod
    def _make_trade_(cls, offer_buy, first_offer_seller, balance_offer_sell, balance_offer_buy, inventory_offer_buy,
                     inventory_offer_sell):
        Trade.objects.create(client=offer_buy.user, client_offer=offer_buy.offer,
                             quantity_client=offer_buy.quantity,
                             price_total=offer_buy.total_price_is_offer,
                             seller=first_offer_seller.user,
                             seller_offer=first_offer_seller,
                             quantity_seller=first_offer_seller.quantity,
                             price_total_1=first_offer_seller.total_price_is_offer)
        if offer_buy.quantity > first_offer_seller.quantity:
            offer_buy.quantity -= first_offer_seller.quantity
            first_offer_seller.quantity -= first_offer_seller.quantity
            balance_offer_buy.balance -= first_offer_seller.total_price_is_offer
            balance_offer_sell.balance += first_offer_seller.total_price_is_offer
            inventory_offer_buy.quantity += first_offer_seller.quantity
            inventory_offer_sell.quantity -= first_offer_seller.quantity
            first_offer_seller.is_activate = False
            first_offer_seller.save()
            offer_buy.save()
            balance_offer_sell.save()
            balance_offer_buy.save()
            inventory_offer_sell.save()
            inventory_offer_buy.save()
            if offer_buy.is_activate:
                first_offer_seller = list(
                    Offer.objects.filter(type_function=2, is_activate=True, is_locked=False,
                                         price__gte=offer_buy.price))
                for offer_sell in first_offer_seller:
                    Trade.objects.create(client=offer_buy.user, client_offer=offer_buy,
                                         quantity_client=offer_buy.quantity,
                                         price_total=offer_buy.total_price_is_offer,
                                         seller=offer_sell.user,
                                         seller_offer=offer_sell,
                                         quantity_seller=offer_sell.quantity,
                                         price_total_1=offer_sell.total_price_is_offer)
                    if not offer_buy.is_activate and balance_offer_buy.balance > offer_sell.total_price_is_offer:
                        if offer_buy.quantity > offer_sell.quantity:
                            offer_buy.quantity -= offer_sell.quantity
                            offer_sell.quantity -= offer_sell.quantity
                            inventory_offer_buy.quantity += offer_sell.quantity
                            inventory_offer_sell.quantity -= offer_sell.quantity
                            balance_offer_buy.balance -= offer_sell.total_price_is_offer
                            balance_offer_sell.balance += offer_sell.total_price_is_offer
                            offer_sell.is_activate = False
                            balance_offer_sell.save()
                            balance_offer_buy.save()
                            inventory_offer_sell.save()
                            inventory_offer_buy.save()
                            offer_sell.save()
                            offer_buy.save()
                        elif offer_buy.quantity < offer_sell.quantity:
                            offer_sell.quantity -= offer_buy.quantity
                            offer_buy.quantity -= offer_buy.quantity
                            inventory_offer_buy.quantity += offer_sell.quantity
                            inventory_offer_sell.quantity -= offer_sell.quantity
                            balance_offer_buy.balance = balance_offer_buy.balans - (
                                    (
                                            offer_sell.total_price_is_offer /
                                            offer_sell.quantity) * offer_buy.quantity)
                            balance_offer_sell.balance = balance_offer_sell.balans + (
                                    (
                                            offer_sell.total_price_is_offer /
                                            offer_sell.quantity) * offer_buy.quantity)
                            offer_buy.is_activate = False
                            balance_offer_sell.save()
                            balance_offer_buy.save()
                            inventory_offer_sell.save()
                            inventory_offer_buy.save()
                            offer_sell.save()
                            offer_buy.save()
                        elif offer_buy.quantity == offer_sell.quantity:
                            offer_buy.quantity -= offer_buy.quantity
                            offer_sell.quantity -= offer_sell.quantity
                            inventory_offer_buy.quantity += offer_sell.quantity
                            inventory_offer_sell.quantity -= offer_sell.quantity
                            balance_offer_buy.balance -= offer_sell.total_price_is_offer
                            balance_offer_sell.balance += offer_sell.total_price_is_offer
                            offer_sell.is_activate = False
                            offer_buy.is_activate = False
                            balance_offer_sell.save()
                            balance_offer_buy.save()
                            inventory_offer_sell.save()
                            inventory_offer_buy.save()
                            offer_sell.save()
                            offer_buy.save()
                    else:
                        continue

        elif offer_buy.quantity < first_offer_seller.quantity:
            first_offer_seller.quantity -= offer_buy.quantity
            offer_buy.quantity -= offer_buy.quantity
            inventory_offer_buy.quantity += first_offer_seller.quantity
            inventory_offer_sell.quantity -= first_offer_seller.quantity
            balance_offer_buy.balance = balance_offer_buy.balans - (
                    (
                            first_offer_seller.total_price_is_offer /
                            first_offer_seller.quantity) * offer_buy.quantity)
            balance_offer_sell.balance = balance_offer_sell.balans + (
                    (
                            first_offer_seller.total_price_is_offer /
                            first_offer_seller.quantity) * offer_buy.quantity)
            offer_buy.is_activate = False
            balance_offer_sell.save()
            balance_offer_buy.save()
            inventory_offer_sell.save()
            inventory_offer_buy.save()
            first_offer_seller.save()
            offer_buy.save()

        elif offer_buy.quantity == first_offer_seller.quantity:
            offer_buy.quantity -= offer_buy.quantity
            first_offer_seller.quantity -= first_offer_seller.quantity
            balance_offer_buy.balance -= first_offer_seller.total_price_is_offer
            balance_offer_sell.balance += first_offer_seller.total_price_is_offer
            inventory_offer_buy.quantity += first_offer_seller.quantity
            inventory_offer_sell.quantity -= first_offer_seller.quantity
            first_offer_seller.is_activate = False
            offer_buy.is_activate = False
            first_offer_seller.save()
            offer_buy.save()
            balance_offer_sell.save()
            balance_offer_buy.save()
            inventory_offer_sell.save()
            inventory_offer_buy.save()
