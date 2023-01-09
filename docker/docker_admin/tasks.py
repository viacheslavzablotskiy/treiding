from __future__ import absolute_import, unicode_literals

from time import sleep

from celery import shared_task, Celery
from celery.schedules import crontab
from django.db.models import Max
from django.db.models.signals import post_save
from django.dispatch import receiver


# (run_every=(crontab(minute=1)))
# @shared_task
# def save(self, *args, **kwargs):
#     self.offer.total_price_is_offer = self.offer.quantity * self.offer.price
#     super(Offer, self).save(*args, **kwargs)

# @shared_task РАБОТАЕТ на 100
# def price():
#     from docker_admin.models import  Offer, Price
#     p = Offer.objects.aggregate(Max("price"))
#     g = Price.objects.all()
#     g = list(g)
#     g = g[0]
#     g.price =  p["price__max"]
#     g.save()
@shared_task
def trade():
    from docker_admin.models import Offer, Trade, Balans
    p = list(Offer.objects.filter(type_function=1))
    g = list(Offer.objects.filter(type_function=2, ).order_by("price"))
    if g and p:
        p = p[0]
        g = g[0]
        Trade.objects.create(client=p.user, client_offer=p, quantity_client=p.quantity,
                             price_total=p.total_price_is_offer, seller=g.user, seller_offer=g,
                             quantity_seller=g.quantity,
                             price_total_1=g.total_price_is_offer)
        l = list(Balans.objects.filter(user=p.user))
        s = list(Balans.objects.filter(user=g.user))
        l = l[0]
        s = s[0]
        if p.quantity > g.quantity:
            p.quantity -= g.quantity
            g.quantity -= g.quantity
            l.balans -= g.total_price_is_offer
            s.balans += g.total_price_is_offer
            l.save()
            s.save()
            g.delete()
            p.save()
        elif p.quantity < g.quantity:
            p.quantity -= p.quantity
            g.quantity -= p.quantity
            l.balans -= g.total_price_is_offer
            s.balans += g.total_price_is_offer
            l.save()
            s.save()
            p.delete()
            g.save()
        elif p.quantity == g.quantity:
            p.quantity -= g.quantity
            g.quantity -= g.quantity
            l.balans -= g.total_price_is_offer
            s.balans += g.total_price_is_offer
            s.save()
            l.save()
            p.delete()
            g.delete()

    else:
        print("офферы закончилсь")



# @shared_task
# def balance():
#     from docker_admin.models import Balans, Trade, Offer
#     p = Offer.objects.filter(type_function=1)
#     g = Offer.objects.filter(type_function=2)
#     l = Trade.objects.filter(client=p.user, seller=g.user)
#     user_1 = Balans.objects.filter(user=p.user)
#     user_2 = Balans.objects.filter(user=g.user)
#     if l.exists():
#         user_1.balans -= g.total_price_is_offer
#         user_1.balans.save()
#         user_2.balans += g.total_price_is_offer
#         user_2.balans.save()
#         p.qunatity -= g.qunatity
#         p.qunatity.save()


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
