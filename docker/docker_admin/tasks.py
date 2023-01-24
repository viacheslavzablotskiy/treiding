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


class Treid:
    def __init__(self):
        from docker_admin.models import Offer
        self.offer_buy = list(Offer.object.filter(type_function=1, is_active=True))
        from docker_admin.models import Offer, Trade
        if self.offer_buy:
            for offer in self.offer_buy:
                self.offer_is_buy = offer
                self.offer_sell = list(Offer.object.filter(type_function=1, is_active=True, price__gte=offer.price))
                if self.offer_sell:
                    self.sell_offer = self.offer_sell[0]
                    Trade.objects.create(client=self.offer_is_buy.user, client_offer=self.offer_is_buy.offer,
                                         quantity_client=self.offer_is_buy.quantity,
                                         price_total=self.offer_is_buy.total_price_is_offer,
                                         seller=self.sell_offer.user,
                                         seller_offer=self.sell_offer,
                                         quantity_seller=self.sell_offer.quantity,
                                         price_total_1=self.sell_offer.total_price_is_offer)

    def calculation(self):
        from docker_admin.models import Balance, Inventory, Trade, Offer
        inventory_offer = list(Inventory.objects.filter(user=self.offer_is_buy.user))
        inventory_offer = inventory_offer[0]
        inventory_offer_sell = list(Inventory.objects.filter(user=self.sell_offer.user))
        inventory_offer_sell = inventory_offer_sell[0]
        balance_offer = list(Balance.objects.filter(user=self.offer_is_buy.user))
        balance_offer = balance_offer[0]
        balance_offer_sell = list(Balance.objects.filter(user=self.sell_offer.user))
        balance_offer_sell = balance_offer_sell[0]
        if self.offer_is_buy.quantity > self.sell_offer.quantity:
            self.offer_is_buy.quantity -= self.sell_offer.quantity
            self.sell_offer.quantity -= self.sell_offer.quantity
            inventory_offer.quantity += inventory_offer_sell.quantity
            inventory_offer_sell.quantity -= inventory_offer_sell.quantity
            balance_offer.balance -= self.sell_offer.total_price_is_offer
            balance_offer_sell.balance += self.sell_offer.total_price_is_offer
            self.sell_offer.is_activate = False
            self.sell_offer.save()
            self.offer_is_buy.save()
            inventory_offer_sell.save()
            inventory_offer.save()
            balance_offer.save()
            balance_offer_sell.save()
            if self.offer_is_buy.is_activate:
                offer_sell = list(
                    Offer.objects.filter(type_function=2, price__gte=self.offer_is_buy.price, is_activate=True))
                for offer_1 in offer_sell:
                    if not offer_1 or not self.offer_is_buy.is_activate:
                        break
                    else:
                        Trade.objects.create(client=self.offer_is_buy.user, client_offer=self.offer_is_buy,
                                             quantity_client=self.offer_is_buy.quantity,
                                             price_total=self.offer_is_buy.total_price_is_offer, seller=offer_1.user,
                                             seller_offer=offer_1,
                                             quantity_seller=offer_1.quantity,
                                             price_total_1=offer_1.total_price_is_offer)
                        inventory_offer = list(Inventory.objects.filter(user=self.offer_is_buy.user))
                        inventory_offer = inventory_offer[0]
                        inventory_offer_sell = list(Inventory.objects.filter(user=offer_1.user))
                        inventory_offer_sell = inventory_offer_sell[0]
                        balance_offer = list(Balance.objects.filter(user=self.offer_is_buy.user))
                        balance_offer = balance_offer[0]
                        balance_offer_sell = list(Balance.objects.filter(user=offer_1.user))
                        balance_offer_sell = balance_offer_sell[0]
                        if self.offer_is_buy.quantity > offer_1.quantity:
                            offer_1.is_activate = False
                            balance_offer.balance -= offer_1.total_price_is_offer
                            balance_offer_sell.balance += offer_1.total_price_is_offer
                            inventory_offer.quantity += offer_1.quantity
                            inventory_offer_sell.quantity -= offer_1.quantity
                            self.offer_is_buy.quantity -= offer_1.quantity
                            offer_1.quantity -= offer_1.quantity
                            balance_offer_sell.save()
                            balance_offer.save()
                            inventory_offer_sell.save()
                            inventory_offer.save()
                            offer_1.save()
                            self.offer_is_buy.save()
                        elif self.offer_is_buy.quantity < offer_1.quantity:
                            self.offer_is_buy.is_activate = False
                            balance_offer.balance = balance_offer.balans - (
                                    (offer_1.total_price_is_offer / offer_1.quantity) * self.offer_is_buy.quantity)
                            balance_offer_sell.balance = balance_offer_sell.balans + (
                                    (offer_1.total_price_is_offer / offer_1.quantity) * self.offer_is_buy.quantity)
                            inventory_offer.quantity += self.offer_is_buy.quantity
                            inventory_offer_sell.quantity -= self.offer_is_buy.quantity
                            offer_1.quantity -= self.offer_is_buy.quantity
                            self.offer_is_buy.quantity -= self.offer_is_buy.quantity
                            balance_offer_sell.save()
                            balance_offer.save()
                            inventory_offer.save()
                            inventory_offer_sell.save()
                            offer_1.save()
                            self.offer_is_buy.save()
                        elif self.offer_is_buy.quantity == offer_1.quantity:
                            balance_offer.balance -= offer_1.total_price_is_offer
                            balance_offer_sell.balance += offer_1.total_price_is_offer
                            offer_1.is_activate = False
                            self.offer_is_buy.is_activate = False
                            inventory_offer_sell.quantity -= self.offer_is_buy.quantity
                            inventory_offer.quantity += offer_1.quantity
                            self.offer_is_buy.quantity -= self.offer_is_buy.quantity
                            offer_1.quantity -= offer_1.quantity
                            balance_offer_sell.save()
                            balance_offer.save()
                            inventory_offer_sell.save()
                            inventory_offer.save()
                            offer_1.save()
                            self.offer_is_buy.save()

    def calculation_1(self):
        from docker_admin.models import Offer, Trade, Balance, Inventory
        inventory_offer = list(Inventory.objects.filter(user=self.offer_is_buy.user))
        inventory_offer = inventory_offer[0]
        inventory_offer_sell = list(Inventory.objects.filter(user=self.sell_offer.user))
        inventory_offer_sell = inventory_offer_sell[0]
        balance_offer = list(Balance.objects.filter(user=self.offer_is_buy.user))
        balance_offer = balance_offer[0]
        balance_offer_sell = list(Balance.objects.filter(user=self.sell_offer.user))
        balance_offer_sell = balance_offer_sell[0]
        if self.offer_is_buy.quantity < self.sell_offer.quantity:
            self.sell_offer.quantity -= self.offer_is_buy.quantity
            self.offer_is_buy.quantity -= self.offer_is_buy.quantity
            inventory_offer.quantity += inventory_offer.quantity
            inventory_offer_sell.quantity -= inventory_offer.quantity
            balance_offer.balance -= (self.sell_offer.total_price_is_offer
                                      / self.sell_offer.quantity) * self.offer_is_buy.quantity
            balance_offer_sell.balance += (self.sell_offer.total_price_is_offer
                                           / self.sell_offer.quantity) * self.offer_is_buy.quantity
            self.offer_is_buy.is_activate = False
            self.sell_offer.save()
            self.offer_is_buy.save()
            inventory_offer_sell.save()
            inventory_offer.save()
            balance_offer.save()
            balance_offer_sell.save()

    def calculation_2(self):
        from docker_admin.models import  Balance, Inventory
        inventory_offer = list(Inventory.objects.filter(user=self.offer_is_buy.user))
        inventory_offer = inventory_offer[0]
        inventory_offer_sell = list(Inventory.objects.filter(user=self.sell_offer.user))
        inventory_offer_sell = inventory_offer_sell[0]
        balance_offer = list(Balance.objects.filter(user=self.offer_is_buy.user))
        balance_offer = balance_offer[0]
        balance_offer_sell = list(Balance.objects.filter(user=self.sell_offer.user))
        balance_offer_sell = balance_offer_sell[0]
        if self.offer_is_buy.quantity == self.sell_offer.quantity:
            self.sell_offer.quantity -= self.sell_offer.quantity
            self.offer_is_buy.quantity -= self.offer_is_buy.quantity
            inventory_offer.quantity += inventory_offer.quantity
            inventory_offer_sell.quantity -= inventory_offer_sell.quantity
            balance_offer.balance -= self.sell_offer.total_price_is_offer
            balance_offer_sell.balance += self.sell_offer.total_price_is_offer
            self.offer_is_buy.is_activate = False
            self.sell_offer.is_activate = False
            self.sell_offer.save()
            self.offer_is_buy.save()
            inventory_offer_sell.save()
            inventory_offer.save()
            balance_offer.save()
            balance_offer_sell.save()

