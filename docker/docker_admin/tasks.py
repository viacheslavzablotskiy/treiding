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
    def find_offer_for_buyer(cls):
        list_offer_buyer = list(Offer.objects.filter(type_function=1, is_activate=True))
        if list_offer_buyer:
            for offer_buy in list_offer_buyer:
                list_offer_seller = list(
                    Offer.objects.filter(type_function=2, is_activate=True,
                                         price__gte=offer_buy.price))
                the_first_offer_seller = list_offer_seller[0]
                balance_offer_buy = list(Balance.objects.filter(user=offer_buy.user))
                balance_offer_buy = balance_offer_buy[0]
                balance_offer_sell = list(Balance.objects.filter(user=the_first_offer_seller.user))
                balance_offer_sell = balance_offer_sell[0]
                inventory_offer = list(Inventory.objects.filter(user=offer_buy.user))
                inventory_offer = inventory_offer[0]
                inventory_offer_sell = list(Inventory.objects.filter(user=the_first_offer_seller.user))
                inventory_offer_sell = inventory_offer_sell[0]
                if the_first_offer_seller and balance_offer_buy.balance > the_first_offer_seller.total_price_is_offer:
                    Trade.objects.create(client=offer_buy.user, client_offer=offer_buy.offer,
                                         quantity_client=offer_buy.quantity,
                                         price_total=offer_buy.total_price_is_offer,
                                         seller=the_first_offer_seller.user,
                                         seller_offer=the_first_offer_seller,
                                         quantity_seller=the_first_offer_seller.quantity,
                                         price_total_1=the_first_offer_seller.total_price_is_offer)

                    cls.changes_job_a_trade(
                        offer_buy=offer_buy, the_first_offer_seller=the_first_offer_seller,
                        balance_offer_buy=balance_offer_buy,
                        balance_offer_sell=balance_offer_sell, inventory_offer=inventory_offer,
                        inventory_offer_sell=inventory_offer_sell
                    )
                else:
                    continue

    @classmethod
    def if_the_buyer_has_more(cls, balance_offer_buy, balance_offer_sell, inventory_offer, inventory_offer_sell,
                              the_first_offer_seller, offer_buy):
        balance_offer_buy.balance -= the_first_offer_seller.total_price_is_offer
        balance_offer_sell.balance += the_first_offer_seller.total_price_is_offer
        offer_buy.quantity -= the_first_offer_seller.quantity
        the_first_offer_seller.quantity -= the_first_offer_seller.quantity
        inventory_offer.quantity += the_first_offer_seller.quantity
        inventory_offer_sell.quantity -= the_first_offer_seller.quantity
        the_first_offer_seller.is_activate = False
        the_first_offer_seller.save()
        offer_buy.save()
        balance_offer_sell.save()
        balance_offer_buy.save()
        inventory_offer_sell.save()
        inventory_offer.save()
        if offer_buy.is_activate:
            cls.if_a_first_offer_not_covers(offer_buy=offer_buy,
                                            the_first_offer_seller
                                            =the_first_offer_seller
                                            )


    @classmethod
    def if_a_first_offer_not_covers(cls, offer_buy, the_first_offer_seller):

        for offer_sell_if_the_first_offer_sell_not_covers in the_first_offer_seller:
            balance_offer_sell = list(Balance.objects.filter(user=offer_sell_if_the_first_offer_sell_not_covers.user))
            balance_offer_sell = balance_offer_sell[0]
            balance_offer = list(Balance.objects.filter(user=offer_buy.user))
            balance_offer = balance_offer[0]
            inventory_offer_sell = list(
                Inventory.objects.filter(user=offer_sell_if_the_first_offer_sell_not_covers.user))
            inventory_offer_sell = inventory_offer_sell[0]
            inventory_offer = list(Inventory.objects.filter(user=offer_buy.user))
            inventory_offer = inventory_offer[0]
            if not offer_sell_if_the_first_offer_sell_not_covers or not offer_buy.is_activate:
                Trade.objects.create(client=offer_buy.user, client_offer=offer_buy,
                                     quantity_client=offer_buy.quantity,
                                     price_total=offer_buy.total_price_is_offer,
                                     seller=offer_sell_if_the_first_offer_sell_not_covers.user,
                                     seller_offer=offer_sell_if_the_first_offer_sell_not_covers,
                                     quantity_seller=offer_sell_if_the_first_offer_sell_not_covers.quantity,
                                     price_total_1=offer_sell_if_the_first_offer_sell_not_covers.total_price_is_offer)
                cls.changes_to_create_a_trade(
                    offer_sell_if_the_first_offer_sell_not_covers=offer_sell_if_the_first_offer_sell_not_covers,
                    balance_offer=balance_offer, balance_offer_sell=balance_offer_sell,
                    inventory_offer=inventory_offer, inventory_offer_sell=inventory_offer_sell, offer_buy=offer_buy)

    @classmethod
    def the_offer_buy_has_more(cls, offer_sell_if_the_first_offer_sell_not_covers, offer_buy, balance_offer_sell,
                               balance_offer,
                               inventory_offer_sell,
                               inventory_offer):
        offer_sell_if_the_first_offer_sell_not_covers.is_activate = False
        balance_offer.balance -= offer_sell_if_the_first_offer_sell_not_covers.total_price_is_offer
        balance_offer_sell.balance += offer_sell_if_the_first_offer_sell_not_covers.total_price_is_offer
        inventory_offer.quantity += offer_sell_if_the_first_offer_sell_not_covers.quantity
        inventory_offer_sell.quantity -= offer_sell_if_the_first_offer_sell_not_covers.quantity
        offer_buy.quantity -= offer_sell_if_the_first_offer_sell_not_covers.quantity
        offer_sell_if_the_first_offer_sell_not_covers.quantity -= offer_sell_if_the_first_offer_sell_not_covers.quantity
        balance_offer_sell.save()
        balance_offer.save()
        inventory_offer_sell.save()
        inventory_offer.save()
        offer_sell_if_the_first_offer_sell_not_covers.save()
        offer_buy.save()


    @classmethod
    def the_offer_seller_2_has_more(cls, offer_sell_if_the_first_offer_sell_not_covers, offer_buy, balance_offer,
                                    balance_offer_sell,
                                    inventory_offer,
                                    inventory_offer_sell):
        offer_buy.is_activate = False
        balance_offer.balance = balance_offer.balans - (
                (
                        offer_sell_if_the_first_offer_sell_not_covers.total_price_is_offer /
                        offer_sell_if_the_first_offer_sell_not_covers.quantity) * offer_buy.quantity)
        balance_offer_sell.balance = balance_offer_sell.balans + (
                (
                        offer_sell_if_the_first_offer_sell_not_covers.total_price_is_offer /
                        offer_sell_if_the_first_offer_sell_not_covers.quantity) * offer_buy.quantity)
        inventory_offer.quantity += offer_buy.quantity
        inventory_offer_sell.quantity -= offer_buy.quantity
        offer_sell_if_the_first_offer_sell_not_covers.quantity -= offer_buy.quantity
        offer_buy.quantity -= offer_buy.quantity
        balance_offer_sell.save()
        balance_offer.save()
        inventory_offer.save()
        inventory_offer_sell.save()
        offer_sell_if_the_first_offer_sell_not_covers.save()
        offer_buy.save()


    @classmethod
    def the_offer_seller_2_and_offer_buy_have_equal(cls, offer_sell_if_the_first_offer_sell_not_covers, offer_buy,
                                                    balance_offer,
                                                    inventory_offer, inventory_offer_sell, balance_offer_sell, ):
        balance_offer.balance -= offer_sell_if_the_first_offer_sell_not_covers.total_price_is_offer
        balance_offer_sell.balance += offer_sell_if_the_first_offer_sell_not_covers.total_price_is_offer
        offer_sell_if_the_first_offer_sell_not_covers.is_activate = False
        offer_buy.is_activate = False
        inventory_offer_sell.quantity -= offer_buy.quantity
        inventory_offer.quantity += offer_sell_if_the_first_offer_sell_not_covers.quantity
        offer_buy.quantity -= offer_buy.quantity
        offer_sell_if_the_first_offer_sell_not_covers.quantity -= offer_sell_if_the_first_offer_sell_not_covers.quantity
        balance_offer_sell.save()
        balance_offer.save()
        inventory_offer_sell.save()
        inventory_offer.save()
        offer_sell_if_the_first_offer_sell_not_covers.save()
        offer_buy.save()


    @classmethod
    def changes_to_create_a_trade(cls,
                                  offer_sell_if_the_first_offer_sell_not_covers,
                                  offer_buy,
                                  balance_offer,
                                  balance_offer_sell,
                                  inventory_offer,
                                  inventory_offer_sell):
        if offer_buy.quantity > offer_sell_if_the_first_offer_sell_not_covers.quantity:
            cls.the_offer_buy_has_more(
                offer_sell_if_the_first_offer_sell_not_covers=offer_sell_if_the_first_offer_sell_not_covers,
                offer_buy=offer_buy,
                balance_offer_sell=balance_offer_sell, inventory_offer=inventory_offer,
                inventory_offer_sell=inventory_offer_sell, balance_offer=balance_offer)
        elif offer_buy.quantity < offer_sell_if_the_first_offer_sell_not_covers.quantity:
            cls.the_offer_seller_2_has_more(
                offer_sell_if_the_first_offer_sell_not_covers=offer_sell_if_the_first_offer_sell_not_covers,
                offer_buy=offer_buy,
                balance_offer_sell=balance_offer_sell, inventory_offer=inventory_offer,
                inventory_offer_sell=inventory_offer_sell, balance_offer=balance_offer)
        elif offer_buy.quantity == offer_sell_if_the_first_offer_sell_not_covers.quantity:
            cls.the_offer_seller_2_and_offer_buy_have_equal(
                offer_sell_if_the_first_offer_sell_not_covers=offer_sell_if_the_first_offer_sell_not_covers,
                offer_buy=offer_buy,
                balance_offer_sell=balance_offer_sell,
                inventory_offer=inventory_offer,
                inventory_offer_sell=inventory_offer_sell,
                balance_offer=balance_offer)

    @classmethod
    def the_buyer_and_seller_have_equal(cls, offer_buy, the_first_offer_seller, balance_offer_buy, balance_offer_sell,
                                        inventory_offer, inventory_offer_sell):

        offer_buy.quantity -= offer_buy.quantity
        the_first_offer_seller.quantity -= the_first_offer_seller.quantity
        inventory_offer.quantity -= offer_buy.quantity
        inventory_offer_sell.quantity -= the_first_offer_seller.quantity
        balance_offer_buy.balance -= the_first_offer_seller.total_price_is_offer
        balance_offer_sell.balance -= the_first_offer_seller.total_price_is_offer
        the_first_offer_seller.is_activate = False
        offer_buy.is_activate = False
        offer_buy.save()
        the_first_offer_seller.save()
        inventory_offer.save()
        inventory_offer_sell.save()
        balance_offer_sell.save()
        balance_offer_buy.save()


    @classmethod
    def the_seller_has_more(cls, offer_buy, the_first_offer_seller, balance_offer_buy, balance_offer_sell,
                            inventory_offer, inventory_offer_sell):
        the_first_offer_seller.quantity -= offer_buy.quantity
        offer_buy.quantity -= offer_buy.quantity
        inventory_offer.quantity += offer_buy.quantity
        inventory_offer_sell.quantity -= the_first_offer_seller.quantity
        balance_offer_buy.balance -= \
            (the_first_offer_seller.total_price_is_offer /
             the_first_offer_seller.quantity) * offer_buy.quantity
        balance_offer_sell.balance += (
                                              the_first_offer_seller.total_price_is_offer /
                                              the_first_offer_seller.quantity) * offer_buy.quantity
        the_first_offer_seller.is_activate = False
        offer_buy.save()
        offer_buy.save()
        balance_offer_sell.save()
        balance_offer_buy.save()
        inventory_offer.save()
        inventory_offer_sell.save()


    @classmethod
    def changes_job_a_trade(cls, offer_buy,
                            the_first_offer_seller,
                            balance_offer_buy,
                            balance_offer_sell,
                            inventory_offer,
                            inventory_offer_sell):
        if offer_buy.quantity > the_first_offer_seller.quantity:
            cls.if_the_buyer_has_more(offer_buy=offer_buy, the_first_offer_seller=the_first_offer_seller,
                                      balance_offer_sell=balance_offer_sell, balance_offer_buy=balance_offer_buy,
                                      inventory_offer=inventory_offer, inventory_offer_sell=inventory_offer_sell)
        elif offer_buy.quantity < the_first_offer_seller.quantity:
            cls.the_seller_has_more(offer_buy=offer_buy, the_first_offer_seller=the_first_offer_seller,
                                    balance_offer_sell=balance_offer_sell, balance_offer_buy=balance_offer_buy,
                                    inventory_offer=inventory_offer, inventory_offer_sell=inventory_offer_sell)
        elif offer_buy.quantity == the_first_offer_seller.quantity:
            cls.the_buyer_and_seller_have_equal(offer_buy=offer_buy,
                                                the_first_offer_seller=the_first_offer_seller,
                                                balance_offer_sell=balance_offer_sell,
                                                balance_offer_buy=balance_offer_buy,
                                                inventory_offer=inventory_offer,
                                                inventory_offer_sell=inventory_offer_sell)
