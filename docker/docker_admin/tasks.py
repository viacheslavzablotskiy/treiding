from __future__ import absolute_import, unicode_literals

from time import sleep

from celery import shared_task, Celery
from celery.schedules import crontab
from django.db.models import Max
from django.db.models.signals import post_save
from django.dispatch import receiver


#
@shared_task
def price():
    from docker_admin.models import Trade, Item
    p = list(Trade.objects.all().order_by("price_total_1"))
    p = p[-1]
    g = list(Item.objects.all())
    g = g[0]
    g.max_price = p.price_total_1
    g.save()

@shared_task
def trade():
    from docker_admin.models import Offer, Balans, Inventory, Trade
    offer_buy = list(Offer.objects.filter(type_function=1, is_activate=True))
    if offer_buy:
        for offer in offer_buy:
            offer_sell = list(Offer.objects.filter(type_function=2, price__lte=offer.price, is_activate=True))
            if offer_sell:
                offer_sell = offer_sell[0]
                Trade.objects.create(client=offer.user, client_offer=offer, quantity_client=offer.quantity,
                                     price_total=offer.total_price_is_offer, seller=offer_sell.user,
                                     seller_offer=offer_sell,
                                     quantity_seller=offer_sell.quantity,
                                     price_total_1=offer_sell.total_price_is_offer)
                inventory_offer = list(Inventory.objects.filter(user=offer.user))
                inventory_offer = inventory_offer[0]
                inventory_offer_sell = list(Inventory.objects.filter(user=offer_sell.user))
                inventory_offer_sell = inventory_offer_sell[0]
                balance_offer = list(Balans.objects.filter(user=offer.user))
                balance_offer = balance_offer[0]
                balance_offer_sell = list(Balans.objects.filter(user=offer_sell.user))
                balance_offer_sell = balance_offer_sell[0]
                if offer.quantity > offer_sell.quantity:
                    offer_sell.is_activate = False
                    balance_offer.balans -= offer_sell.total_price_is_offer
                    balance_offer_sell.balans += offer_sell.total_price_is_offer
                    inventory_offer.quantity += offer_sell.quantity
                    inventory_offer_sell.quantity -= offer_sell.quantity
                    offer.quantity -= offer_sell.quantity
                    offer_sell.quantity -= offer_sell.quantity
                    balance_offer_sell.save()
                    balance_offer.save()
                    inventory_offer_sell.save()
                    inventory_offer.save()
                    offer_sell.save()
                    offer.save()
                    if offer.is_activate and offer_sell:
                        offer_sell = list(
                            Offer.objects.filter(type_function=2, price__lte=offer.price, is_activate=True))
                        for offer_1 in offer_sell:
                            if not offer_1 or not offer.is_activate:
                                break
                            else:
                                Trade.objects.create(client=offer.user, client_offer=offer, quantity_client=offer.quantity,
                                                     price_total=offer.total_price_is_offer, seller=offer_1.user,
                                                     seller_offer=offer_1,
                                                     quantity_seller=offer_1.quantity,
                                                     price_total_1=offer_1.total_price_is_offer)
                                inventory_offer = list(Inventory.objects.filter(user=offer.user))
                                inventory_offer = inventory_offer[0]
                                inventory_offer_sell = list(Inventory.objects.filter(user=offer_1.user))
                                inventory_offer_sell = inventory_offer_sell[0]
                                balance_offer = list(Balans.objects.filter(user=offer.user))
                                balance_offer = balance_offer[0]
                                balance_offer_sell = list(Balans.objects.filter(user=offer_1.user))
                                balance_offer_sell = balance_offer_sell[0]
                                if offer.quantity > offer_1.quantity:
                                    offer_1.is_activate = False
                                    balance_offer.balans -= offer_1.total_price_is_offer
                                    balance_offer_sell.balans += offer_1.total_price_is_offer
                                    inventory_offer.quantity += offer_1.quantity
                                    inventory_offer_sell.quantity -= offer_1.quantity
                                    offer.quantity -= offer_1.quantity
                                    offer_1.quantity -= offer_1.quantity
                                    balance_offer_sell.save()
                                    balance_offer.save()
                                    inventory_offer_sell.save()
                                    inventory_offer.save()
                                    offer_1.save()
                                    offer.save()
                                elif offer.quantity < offer_1.quantity:
                                    offer.is_activate = False
                                    balance_offer.balans = balance_offer.balans - (
                                                (offer_1.total_price_is_offer / offer_1.quantity) * offer.quantity)
                                    balance_offer_sell.balans = balance_offer_sell.balans + (
                                                (offer_1.total_price_is_offer / offer_1.quantity) * offer.quantity)
                                    inventory_offer.quantity += offer.quantity
                                    inventory_offer_sell.quantity -= offer.quantity
                                    offer_1.quantity -= offer.quantity
                                    offer.quantity -= offer.quantity
                                    balance_offer_sell.save()
                                    balance_offer.save()
                                    inventory_offer.save()
                                    inventory_offer_sell.save()
                                    offer_1.save()
                                    offer.save()
                                elif offer.quantity == offer_1.quantity:
                                    balance_offer.balans -= offer_1.total_price_is_offer
                                    balance_offer_sell.balans += offer_1.total_price_is_offer
                                    offer_1.is_activate = False
                                    offer.is_activate = False
                                    inventory_offer_sell.quantity -= offer.quantity
                                    inventory_offer.quantity += offer_1.quantity
                                    offer.quantity -= offer.quantity
                                    offer_1.quantity -= offer_1.quantity
                                    balance_offer_sell.save()
                                    balance_offer.save()
                                    inventory_offer_sell.save()
                                    inventory_offer.save()
                                    offer_1.save()
                                    offer.save()

                    else:
                        continue
                elif offer.quantity < offer_sell.quantity:
                    offer.is_activate = False
                    balance_offer.balans = balance_offer.balans - ((offer_sell.total_price_is_offer / offer_sell.quantity) * offer.quantity)
                    balance_offer_sell.balans = balance_offer_sell.balans + ((offer_sell.total_price_is_offer / offer_sell.quantity) * offer.quantity)
                    inventory_offer.quantity += offer.quantity
                    inventory_offer_sell.quantity -= offer.quantity
                    offer_sell.quantity -= offer.quantity
                    offer.quantity -= offer.quantity
                    balance_offer_sell.save()
                    balance_offer.save()
                    inventory_offer.save()
                    inventory_offer_sell.save()
                    offer_sell.save()
                    offer.save()
                elif offer.quantity == offer_sell.quantity:
                    balance_offer.balans -= offer_sell.total_price_is_offer
                    balance_offer_sell.balans += offer_sell.total_price_is_offer
                    offer_sell.is_activate = False
                    offer.is_activate = False
                    inventory_offer_sell.quantity -= offer.quantity
                    inventory_offer.quantity += offer_sell.quantity
                    offer.quantity -= offer.quantity
                    offer_sell.quantity -= offer_sell.quantity
                    balance_offer_sell.save()
                    balance_offer.save()
                    inventory_offer_sell.save()
                    inventory_offer.save()
                    offer_sell.save()
                    offer.save()


            else:
                continue
    else:
        print("офферы закончились")

# проверить баланс для каждого случая 1 YES
# а также установить модель inventory 2 YES
# еще больше влиться в данную таску и попробывать сделать чтото с цикло
# понять как работает одноременно несоклько тасок через  какое либо время
# узнать больше о докере как описание контейнера
# научиться подключаться к любой базе данных а не тольок к дефолтной postgres
# повторить работу со словарями
# узнать больше о классах представления
# а также изучить pytest

# @shared_task
# def offer():
#     from docker_admin.models import Offer
#     offer = list(Offer.objects.filter(quantity=0.00))
#     for i in offer:
#         i.delete()

# balance_offer = list(Balans.objects.filter(user=offer.user))
#                     balance_offer = balance_offer[0]
#                     inventory_offer = list(Inventory.objects.filter(user=offer.user))
#                     inventory_offer = inventory_offer[0]
#                     balance_offer_sell = list(Balans.objects.filter(user=offer_sell.user))
#                     balance_offer_sell = balance_offer_sell[0]
#                     inventory_offer_sell = list(Inventory.objects.filter(user=offer_sell.user))
#                     inventory_offer_sell = inventory_offer_sell[0]
#                     if offer.quantity > offer_sell.quantity:
#                         inventory_offer.quantity += offer_sell.quantity
#                         inventory_offer_sell.quantity -= offer_sell.quantity
#                         balance_offer.balans = balance_offer.balans - offer_sell.total_price_is_offer
#                         balance_offer_sell.balans = balance_offer_sell.balans + offer_sell.total_price_is_offer
#                         offer.quantity -= offer_sell.quantity
#                         offer_sell.quantity -= offer_sell.quantity
#                         inventory_offer_sell.save()
#                         inventory_offer.save()
#                         balance_offer_sell.save()
#                         balance_offer.save()
#                         offer.save()
#                         offer_sell.delete()
#                     elif offer.quantity < offer_sell.quantity:
#                         inventory_offer.quantity += offer.quantity
#                         inventory_offer_sell.quantity -= offer.quantity
#                         count =(offer_sell.total_price_is_offer / offer_sell.quantity) * offer.quantity
#                         offer.quantity -= offer.quantity
#                         offer_sell.quantity -= offer.quantity
#                         balance_offer.balans = balance_offer.balans - count
#                         balance_offer_sell.balans = balance_offer_sell.balans + count
#                         balance_offer_sell.save()
#                         balance_offer.save()
#                         inventory_offer.save()
#                         inventory_offer_sell.save()
#                         offer_sell.save()
#                         offer.delete()
#                     elif offer.quantity == offer_sell.quantity:
#                         inventory_offer.quantity += offer_sell.quantity
#                         inventory_offer_sell.quantity -= offer.quantity
#                         balance_offer_sell.balans = balance_offer_sell.balans + offer_sell.total_price_is_offer
#                         balance_offer.balans = balance_offer.balans - offer_sell.total_price_is_offer
#                         offer.quantity -= offer_sell.quantity
#                         offer_sell.quantity -= offer.quantity
#                         inventory_offer.save()
#                         inventory_offer_sell.save()
#                         balance_offer_sell.save()
#                         balance_offer.save()
#                         offer_sell.delete()
#                         offer.delete()
#
# balance_offer = list(Balans.objects.filter(user=offer_buy.user))
#                     balance_offer = balance_offer[0]
#                     inventory_offer = list(Inventory.objects.filter(user=offer_buy.user))
#                     inventory_offer = inventory_offer[0]
#                     balance_offer_buy = list(Balans.objects.filter(user=offer.user))
#                     balance_offer_buy = balance_offer_buy[0]
#                     inventory_offer_buy = list(Inventory.objects.filter(user=offer.user))
#                     inventory_offer_buy = inventory_offer_buy[0]
#                     if offer_buy.quantity > offer.quantity:
#                         inventory_offer_buy.quantity += offer.quantity
#                         inventory_offer.quantity -= offer.quantity
#                         balance_offer_buy.balans = balance_offer_buy.balans - offer.total_price_is_offer
#                         balance_offer.balans = balance_offer.balans + offer.total_price_is_offer
#                         offer_buy.quantity -= offer.quantity
#                         offer.quantity -= offer.quantity
#                         inventory_offer.save()
#                         inventory_offer_buy.save()
#                         balance_offer_buy.save()
#                         balance_offer.save()
#                         offer_buy.save()
#                         offer.delete()
#                     elif offer_buy.quantity < offer.quantity:
#                         inventory_offer_buy.quantity += offer_buy.quantity
#                         inventory_offer.quantity -= offer_buy.quantity
#                         count = (offer.total_price_is_offer / offer.quantity) * offer_buy.quantity
#                         balance_offer_buy.balans = balance_offer_buy.balans + count
#                         balance_offer.balans = balance_offer.balans - count
#                         offer_buy.quantity -= offer_buy.quantity
#                         offer.quantity -= offer_buy.quantity
#                         inventory_offer.save()
#                         inventory_offer_buy.save()
#                         balance_offer_buy.save()
#                         balance_offer.save()
#                         offer.save()
#                         offer_buy.delete()
#                     elif offer.quantity == offer_buy.quantity:
#                         inventory_offer_buy.quantity += offer.quantity
#                         inventory_offer.quantity -= offer_buy.quantity
#                         balance_offer_buy.balans = balance_offer_buy.balans - offer.total_price_is_offer
#                         balance_offer.balans = balance_offer.balans + offer.total_price_is_offer
#                         offer_buy.quantity -= offer.quantity
#                         offer.quantity -= offer_buy.quantity
#                         inventory_offer.save()
#                         inventory_offer_buy.save()
#                         balance_offer_buy.save()
#                         balance_offer.save()
#                         offer.delete()
#                         offer_buy.delete()
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
