from __future__ import absolute_import, unicode_literals

from time import sleep

from celery import shared_task, Celery
from celery.schedules import crontab
from django.db.models import Max
from django.db.models.signals import post_save
from django.dispatch import receiver

@shared_task
def price():
    from docker_admin.models import Offer, Item
    p = Offer.objects.aggregate(Max("price"))
    g = Item.objects.all()
    g = list(g)
    g = g[0]
    g.price_max = p["price__max"]
    g.save()



@shared_task
def trade():
    from docker_admin.models import Offer, Trade, Balans, Inventory
    p = list(Offer.objects.filter(type_function=1))
    g = list(Offer.objects.filter(type_function=2, ).order_by("price"))
    if g and p:
        g = g[0]
        for i in p:
            u = list(Balans.objects.filter(user=i.user))
            u = u[0]
            if u.balans > g.total_price_is_offer:
                Trade.objects.create(client=i.user, client_offer=i, quantity_client=i.quantity,
                                     price_total=i.total_price_is_offer, seller=g.user, seller_offer=g,
                                     quantity_seller=g.quantity,
                                     price_total_1=g.total_price_is_offer)
                s = list(Balans.objects.filter(user=g.user))
                s = s[0]
                if i.quantity > g.quantity:
                    i.quantity -= g.quantity
                    g.quantity -= g.quantity
                    u.balans -= g.total_price_is_offer
                    s.balans += g.total_price_is_offer
                    u.save()
                    s.save()
                    g.delete()
                    i.save()
                elif i.quantity < g.quantity:
                    i.quantity -= i.quantity
                    g.quantity -= i.quantity
                    u.balans -= g.total_price_is_offer
                    s.balans += g.total_price_is_offer
                    u.save()
                    s.save()
                    i.delete()
                    g.save()
                elif i.quantity == g.quantity:
                    i.quantity -= g.quantity
                    g.quantity -= g.quantity
                    u.balans -= g.total_price_is_offer
                    s.balans += g.total_price_is_offer
                    s.save()
                    u.save()
                    i.delete()
                    g.delete()
            else:
                continue
    else:
        print("офферы закончилсь")

# @shared_task
# def inventory():
#     from docker_admin.models import Trade, Inventory
#     p = list(Trade.objects.all())
#     for i in p:
#         if i.client_offer == None or  i.client_offer == None and i.seller_offer == None:
#             s = list(Inventory.objects.filter(user=i.client))
#             seller = list(Inventory.objects.filter(user=i.seller))
#             s = s[0]
#             seller = seller[0]
#             g = Trade.objects.filter(client=s.user).count()
#             s.quantity += g.quantity_seller
#             seller.quantity -= g.quantity_seller
#             s.save()
#         elif i.seller_offer == None:
#             s = Inventory.objects.filter(user=i.client)
#             seller = list(Inventory.objects.filter(user=i.seller))
#             seller =seller[0]
#             s = s[0]
#             g = Trade.objects.filter(client=s.client).count()
#             s.quantity += g.quantity_client
#             seller.quantity -= g.quantity_seller
#             s.save()









