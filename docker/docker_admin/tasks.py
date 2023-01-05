from __future__ import absolute_import, unicode_literals

from time import sleep
from .models import *
from celery import shared_task, Celery
from celery.schedules import crontab


# (run_every=(crontab(minute=1)))
# @shared_task
# def save(self, *args, **kwargs):
#     self.offer.total_price_is_offer = self.offer.quantity * self.offer.price
#     super(Offer, self).save(*args, **kwargs)

@shared_task
def trade():
    # price = 50.00
    # number = 40.00
    # price_number = number + price
    p = Price.objects.filter(price=300.00)
    if p.exists():
        Price.objects.create(price=900.00)
    # type_function = self.offer.type_function
    # quantity = self.offer.quantity
    # price = self.offer.price
    # user = self.offer.user
    # number = 4
    # price_is_offer = 40
    # offer_item = self.offer.item
    # if Offer.objects.filter(user="zlava", quantity=number, price=price_is_offer, type_function=1,
    #                         item=1).exists():
    #     Offer.objects.create(user="vlad", quantity=number, price=number,type_function=1, item=2)
    # trade_client_offer_type_1 = self.trade.client_offer.type_function
    # trade_client_offer_type_2 = self.trade.seller_offer.type_function
    # trade_name_promotion_1 = self.trade.client_offer.item.name
    # trade_name_promotion_2 = self.trade.seller_offer.item.name
    # seller_name = self.user.client_offer
    # client_name = self.user.seller_offer
    # price_promotion_2 = self.user.client_offer.price
    # balance = self.user.client.balans.balans
    # balance_1 = self.user.seller.balans.balans
    # trade_quantity = self.trade.client_offer.quantity
    # trade_quantity_seller = self.trade.seller_offer.quantity
    #
    # if (trade_client_offer_type_1 == 1 and trade_client_offer_type_2 == 2) \
    #     and (trade_name_promotion_2 == trade_name_promotion_1):
    #     seller_total_price = trade_quantity_seller * price_promotion_2
    #     self.trade.price_total_1 = seller_total_price
    #     balance_1 += seller_total_price
    #     balance -= seller_total_price
    #     self.seller = seller_name
    #     self.client = client_name
    #     trade_quantity -= trade_quantity_seller
    #     trade_quantity_seller -= trade_quantity_seller
    #     Trade.objects.create(client=client_name, client_offer=trade_name_promotion_1, quantity_client=trade_quantity,
    #                         price_total=seller_total_price,
    #                          seller=seller_name, seller_offer=trade_name_promotion_2, price_total_1 =seller_total_price,
    #                          quantity_seller= trade_quantity_seller)










# def trade():
#     try:
#         if Offer.objects.get(choices="BUY") or Offer.objects.get(choices="ADD"):
#             print("hello")
#     except:
#         raise ValueError("Данного офера нету ")
