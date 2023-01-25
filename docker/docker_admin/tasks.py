from __future__ import absolute_import, unicode_literals

import logging
from abc import ABC
from time import sleep

import celery
from celery import shared_task, Celery
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from docker.celery import app


@app.task
def send_verification_email(user_id):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
        send_mail(
            'Verify your QuickPublisher account',
            'Follow this link to verify your account: '
            'http://localhost:8000%s' % reverse('verify', kwargs={'uuid': str(user.verification_uuid)}),
            'zlava.mag@gmial.com',
            [user.email],
            fail_silently=False,
        )
    except UserModel.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)

    @shared_task
    def price():
        from docker_admin.models import Trade, Item
        p = list(Trade.objects.all().order_by("price_total_1"))
        if p:
            p = p[-1]
            g = list(Item.objects.all())
            g = g[0]
            g.max_price = p.price_total_1
            g.save()
        else:
            print('не было не одной покупки')


class Procces:
    @classmethod
    def look_offer_to_sell(cls):
        from docker_admin.models import Trade, Offer
        offer_buy_offer = list(Offer.objects.filter(type_function=1, is_activate=True))
        offer_is_buy = offer_buy_offer
        if offer_is_buy:
            for offer_buy in offer_is_buy:
                cls.balance_offer_buy_and_sell(offer_buy=offer_buy)
                cls.offer_edit(offer_buy=offer_buy)
                cls.offer_edit_1(offer_buy=offer_buy)
                offer_seller = list(Offer.objects.filter(type_function=2, is_activate=True, price__gte=offer_buy.price))
                if offer_seller:
                    offer_seller = offer_seller[0]
                    cls.offer_edit(offer_seller=offer_seller)
                    cls.balance_offer_buy_and_sell(offer_seller=offer_seller)
                    cls.offer_edit_1(offer_seller=offer_seller)
                    Trade.objects.create(client=offer_buy.user, client_offer=offer_buy.offer,
                                         quantity_client=offer_buy.quantity,
                                         price_total=offer_buy.total_price_is_offer,
                                         seller=offer_seller.user,
                                         seller_offer=offer_seller,
                                         quantity_seller=offer_seller.quantity,
                                         price_total_1=offer_seller.total_price_is_offer)

    @classmethod
    def balance_offer_buy_and_sell(cls, offer_buy, offer_seller):
        from docker_admin.models import Balance, Inventory, Offer, Trade
        balance_offer_buy = list(Balance.objects.filter(user=offer_buy.user))
        balance_offer_buy = balance_offer_buy[0]
        balance_offer_sell = list(Balance.objects.filter(user=offer_seller.user))
        balance_offer_sell = balance_offer_sell[0]
        inventory_offer = list(Inventory.objects.filter(user=offer_buy.user))
        inventory_offer = inventory_offer[0]
        inventory_offer_sell = list(Inventory.objects.filter(user=offer_seller.user))
        inventory_offer_sell = inventory_offer_sell[0]
        if offer_buy.quantity > offer_seller.quantity:
            balance_offer_buy.balance -= offer_seller.total_price_is_offer
            balance_offer_sell.balance += offer_seller.total_price_is_offer
            offer_buy.quantity -= offer_seller.quantity
            offer_seller.quantity -= offer_seller.quantity
            inventory_offer.quantity += offer_seller.quantity
            inventory_offer_sell.quantity -= offer_seller.quantity
            offer_seller.is_activate = False
            offer_seller.save()
            offer_buy.save()
            balance_offer_sell.save()
            balance_offer_buy.save()
            inventory_offer_sell.save()
            inventory_offer.save()
            if offer_buy.is_activate:
                offer_seller = list(Offer.objects.filter(type_function=2, price__gte=offer_buy.price, is_activate=True))
                for offer_1 in offer_seller:
                    if not offer_1 or not offer_buy.is_activate:
                        Trade.objects.create(client=offer_buy.user, client_offer=offer_buy,
                                             quantity_client=offer_buy.quantity,
                                             price_total=offer_buy.total_price_is_offer, seller=offer_1.user,
                                             seller_offer=offer_1,
                                             quantity_seller=offer_1.quantity,
                                             price_total_1=offer_1.total_price_is_offer)
                        inventory_offer = list(Inventory.objects.filter(user=offer_buy.user))
                        inventory_offer = inventory_offer[0]
                        inventory_offer_sell = list(Inventory.objects.filter(user=offer_1.user))
                        inventory_offer_sell = inventory_offer_sell[0]
                        balance_offer = list(Balance.objects.filter(user=offer_buy.user))
                        balance_offer = balance_offer[0]
                        balance_offer_sell = list(Balance.objects.filter(user=offer_1.user))
                        balance_offer_sell = balance_offer_sell[0]
                        if offer_buy.quantity > offer_1.quantity:
                            offer_1.is_activate = False
                            balance_offer.balance -= offer_1.total_price_is_offer
                            balance_offer_sell.balance += offer_1.total_price_is_offer
                            inventory_offer.quantity += offer_1.quantity
                            inventory_offer_sell.quantity -= offer_1.quantity
                            offer_buy.quantity -= offer_1.quantity
                            offer_1.quantity -= offer_1.quantity
                            balance_offer_sell.save()
                            balance_offer.save()
                            inventory_offer_sell.save()
                            inventory_offer.save()
                            offer_1.save()
                            offer_buy.save()
                        elif offer_buy.quantity < offer_1.quantity:
                            offer_buy.is_activate = False
                            balance_offer.balance = balance_offer.balans - (
                                    (offer_1.total_price_is_offer / offer_1.quantity) * offer_buy.quantity)
                            balance_offer_sell.balance = balance_offer_sell.balans + (
                                    (offer_1.total_price_is_offer / offer_1.quantity) * offer_buy.quantity)
                            inventory_offer.quantity += offer_buy.quantity
                            inventory_offer_sell.quantity -= offer_buy.quantity
                            offer_1.quantity -= offer_buy.quantity
                            offer_buy.quantity -= offer_buy.quantity
                            balance_offer_sell.save()
                            balance_offer.save()
                            inventory_offer.save()
                            inventory_offer_sell.save()
                            offer_1.save()
                            offer_buy.save()
                        elif offer_buy.quantity == offer_1.quantity:
                            balance_offer.balance -= offer_1.total_price_is_offer
                            balance_offer_sell.balance += offer_1.total_price_is_offer
                            offer_1.is_activate = False
                            offer_buy.is_activate = False
                            inventory_offer_sell.quantity -= offer_buy.quantity
                            inventory_offer.quantity += offer_1.quantity
                            offer_buy.quantity -= offer_buy.quantity
                            offer_1.quantity -= offer_1.quantity
                            balance_offer_sell.save()
                            balance_offer.save()
                            inventory_offer_sell.save()
                            inventory_offer.save()
                            offer_1.save()
                            offer_buy.save()

    @classmethod
    def offer_edit(cls, offer_buy, offer_seller):
        from docker_admin.models import Offer, Trade, Inventory, Balance
        balance_offer_buy = list(Balance.objects.filter(user=offer_buy.user))
        balance_offer_buy = balance_offer_buy[0]
        balance_offer_sell = list(Balance.objects.filter(user=offer_seller.user))
        balance_offer_sell = balance_offer_sell[0]
        inventory_offer = list(Inventory.objects.filter(user=offer_buy.user))
        inventory_offer = inventory_offer[0]
        inventory_offer_sell = list(Inventory.objects.filter(user=offer_seller.user))
        inventory_offer_sell = inventory_offer_sell[0]
        if offer_buy.quantity < offer_seller.quantity:
            offer_seller.quantity -= offer_buy.quantity
            offer_buy.quantity -= offer_buy.quantity
            inventory_offer.quantity += offer_buy.quantity
            inventory_offer_sell.quantity -= offer_seller.quantity
            balance_offer_buy.balance -= (
                    offer_seller.total_price_is_offer / offer_seller.quantity) * offer_buy.quantity
            balance_offer_sell.balance += (
                    offer_seller.total_price_is_offer / offer_seller.quantity) * offer_buy.quantity
            offer_seller.is_activate = False
            offer_buy.save()
            offer_buy.save()
            balance_offer_sell.save()
            balance_offer_buy.save()
            inventory_offer.save()
            inventory_offer_sell.save()

    @classmethod
    def offer_edit_1(cls, offer_buy, offer_seller):
        from docker_admin.models import Offer, Trade, Inventory, Balance
        balance_offer_buy = list(Balance.objects.filter(user=offer_buy.user))
        balance_offer_buy = balance_offer_buy[0]
        balance_offer_sell = list(Balance.objects.filter(user=offer_seller.user))
        balance_offer_sell = balance_offer_sell[0]
        inventory_offer = list(Inventory.objects.filter(user=offer_buy.user))
        inventory_offer = inventory_offer[0]
        inventory_offer_sell = list(Inventory.objects.filter(user=offer_seller.user))
        inventory_offer_sell = inventory_offer_sell[0]
        if offer_buy.quantity == offer_seller.quantity:
            offer_buy.quantity -= offer_buy.quantity
            offer_seller.quantity -= offer_seller.quantity
            inventory_offer.quantity -= offer_buy.quantity
            inventory_offer_sell.quantity -= offer_seller.quantity
            balance_offer_buy.balance -= offer_seller.total_price_is_offer
            balance_offer_sell.balance -= offer_seller.total_price_is_offer
            offer_seller.is_activate = False
            offer_buy.is_activate = False
            offer_buy.save()
            offer_seller.save()
            inventory_offer.save()
            inventory_offer_sell.save()
            balance_offer_sell.save()
            balance_offer_buy.save()
