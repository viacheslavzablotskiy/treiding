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
from rest_framework.authtoken.models import Token

from docker.celery import app


@shared_task
def create_offer():
    from docker_admin.models import Offer, Inventory
    offer_sell = list(Offer.objects.filter(type_function=2, is_activate=True))
    for offer in offer_sell:
        if not offer.is_activate:
            continue
        else:
            offer_buy = list(Inventory.objects.filter(user=offer.user))
            offer_buy = offer_buy[0]
            if offer.quantity > offer_buy.quantity:
                offer.is_activate = False
                offer.save()
            else:
                offer_buy.quantity = offer_buy.quantity - offer.quantity
                offer.save()


@app.task
def send_verification_email(user_id):
    global UserModel
    try:
        UserModel = get_user_model()
        user = UserModel.objects.get(pk=user_id)
        user_token = list(Token.objects.filter(user=user))
        user_token = user_token[0]
        send_mail(
            'Verify your QuickPublisher account',
            'Follow this link to verify your account: '
            'http://localhost:8000%s' % reverse('verify', kwargs={'key': str(user_token.key)}),
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


class Make_trades:
    @classmethod
    def _looks_for_seller_for_buyers_and_make_trade_(cls):
        global offer_seller, offer_buy
        from docker_admin.models import Trade, Offer, Balance
        offer_buy_offer = list(Offer.objects.filter(type_function=1, is_activate=True))
        offer_is_buy = offer_buy_offer
        if offer_is_buy:
            for offer_buy in offer_is_buy:
                cls.if_the_buyer_has_more_(offer_buy=offer_buy)
                cls.if_the_seller_has_more(offer_buy=offer_buy)
                cls.is_the_buyer_and_the_seller_have_equal_(offer_buy=offer_buy)
                offer_seller = list(Offer.objects.filter(type_function=2, is_activate=True, price__gte=offer_buy.price))
                if offer_seller:
                    offer_seller = offer_seller[0]
                    balance_request_user = list(Balance.objects.filter(user=offer_buy))
                    balance_request_user = balance_request_user[0]
                    if offer_seller.total_price_is_offer < balance_request_user.balance:
                        cls.if_the_buyer_has_more_(offer_seller=offer_seller)
                        cls.if_the_seller_has_more(offer_seller=offer_seller)
                        cls.is_the_buyer_and_the_seller_have_equal_(offer_seller=offer_seller)
                        cls.if_the_first_offer_for_buyer_do_not_covers_the_offer_seller(offer_seller=offer_seller)
                        Trade.objects.create(client=offer_buy.user, client_offer=offer_buy.offer,
                                             quantity_client=offer_buy.quantity,
                                             price_total=offer_buy.total_price_is_offer,
                                             seller=offer_seller.user,
                                             seller_offer=offer_seller,
                                             quantity_seller=offer_seller.quantity,
                                             price_total_1=offer_seller.total_price_is_offer)
                    else:
                        continue
        return cls.if_the_buyer_more_if_the_seller_more_ore_has_equal(offer_buy, offer_seller)

    @classmethod
    def if_the_buyer_has_more_(cls, offer_buy, offer_seller):
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
            cls.if_the_first_offer_for_buyer_do_not_covers_the_offer_seller(offer_buy=offer_buy)
            if offer_buy.is_activate:
                return cls.if_the_first_offer_for_buyer_do_not_covers_the_offer_seller(offer_buy, offer_seller)

    @classmethod
    def if_the_first_offer_for_buyer_do_not_covers_the_offer_seller(cls, offer_buy, offer_seller):
        global offer_1
        from docker_admin.models import Trade, Balance, Inventory
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
        return offer_1, offer_buy

    @classmethod
    def if_the_seller_has_more(cls, offer_buy, offer_seller):
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

        return offer_seller, offer_buy

    @classmethod
    def is_the_buyer_and_the_seller_have_equal_(cls, offer_buy, offer_seller):
        from docker_admin.models import Offer, Trade, Inventory, Balance
        cls.if_the_buyer_more_if_the_seller_more_ore_has_equal(offer_buy=offer_buy, offer_seller=offer_seller)
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
        return offer_seller, offer_buy

    @classmethod
    def if_the_buyer_more_if_the_seller_more_ore_has_equal(cls, offer_buy, offer_seller):
        if offer_buy.quantity > offer_seller.quantity:
            return cls.if_the_buyer_has_more_(offer_buy, offer_seller)
        elif offer_buy.quantity < offer_seller.quantity:
            return cls.if_the_seller_has_more(offer_buy, offer_seller)
        elif offer_buy.quantity == offer_seller.quantity:
            return cls.if_the_buyer_more_if_the_seller_more_ore_has_equal(offer_buy, offer_seller)
        return offer_seller, offer_buy
