from rest_framework.authtoken.models import Token


# def trade():
#     from docker_admin.models import Offer, Balance, Inventory, Trade
#     offer_buy = list(Offer.objects.filter(type_function=1, is_activate=True))
#     if offer_buy:
#         for offer in offer_buy:
#             offer_sell = list(Offer.objects.filter(type_function=2, price__lte=offer.price, is_activate=True))
#             if offer_sell:
#                 offer_sell = offer_sell[0]
#                 Trade.objects.create(client=offer.user, client_offer=offer, quantity_client=offer.quantity,
#                                      price_total=offer.total_price_is_offer, seller=offer_sell.user,
#                                      seller_offer=offer_sell,
#                                      quantity_seller=offer_sell.quantity,
#                                      price_total_1=offer_sell.total_price_is_offer)
#                 inventory_offer = list(Inventory.objects.filter(user=offer.user))
#                 inventory_offer = inventory_offer[0]
#                 inventory_offer_sell = list(Inventory.objects.filter(user=offer_sell.user))
#                 inventory_offer_sell = inventory_offer_sell[0]
#                 balance_offer = list(Balance.objects.filter(user=offer.user))
#                balance_offer = balance_offer[0]
#                 balance_offer_sell = list(Balance.objects.filter(user=offer_sell.user))
#                 balance_offer_sell = balance_offer_sell[0]
#                 if offer.quantity > offer_sell.quantity:
#                     offer_sell.is_activate = False
#                     balance_offer.balance -= offer_sell.total_price_is_offer
#                     balance_offer_sell.balance += offer_sell.total_price_is_offer
#                     inventory_offer.quantity += offer_sell.quantity
#                     inventory_offer_sell.quantity -= offer_sell.quantity
#                     offer.quantity -= offer_sell.quantity
#                     offer_sell.quantity -= offer_sell.quantity
#                     balance_offer_sell.save()
#                     balance_offer.save()
#                     inventory_offer_sell.save()
#                     inventory_offer.save()
#                     offer_sell.save()
#                     offer.save()
#                     if offer.is_activate and offer_sell:
#                         offer_sell = list(
#                             Offer.objects.filter(type_function=2, price__lte=offer.price, is_activate=True))
#                         for offer_1 in offer_sell:
#                             if not offer_1 or not offer.is_activate:
#                                 break
#                             else:
#                                 Trade.objects.create(client=offer.user, client_offer=offer,
#                                                      quantity_client=offer.quantity,
#                                                      price_total=offer.total_price_is_offer, seller=offer_1.user,
#                                                      seller_offer=offer_1,
#                                                      quantity_seller=offer_1.quantity,
#                                                      price_total_1=offer_1.total_price_is_offer)
#                                 inventory_offer = list(Inventory.objects.filter(user=offer.user))
#                                 inventory_offer = inventory_offer[0]
#                                 inventory_offer_sell = list(Inventory.objects.filter(user=offer_1.user))
#                                 inventory_offer_sell = inventory_offer_sell[0]
#                                 balance_offer = list(Balance.objects.filter(user=offer.user))
#                                 balance_offer = balance_offer[0]
#                                 balance_offer_sell = list(Balance.objects.filter(user=offer_1.user))
#                                 balance_offer_sell = balance_offer_sell[0]
#                                 if offer.quantity > offer_1.quantity:
#                                     offer_1.is_activate = False
#                                     balance_offer.balance -= offer_1.total_price_is_offer
#                                     balance_offer_sell.balance += offer_1.total_price_is_offer
#                                     inventory_offer.quantity += offer_1.quantity
#                                     inventory_offer_sell.quantity -= offer_1.quantity
#                                     offer.quantity -= offer_1.quantity
#                                     offer_1.quantity -= offer_1.quantity
#                                     balance_offer_sell.save()
#                                     balance_offer.save()
#                                     inventory_offer_sell.save()
#                                     inventory_offer.save()
#                                     offer_1.save()
#                                     offer.save()
#                                 elif offer.quantity < offer_1.quantity:
#                                     offer.is_activate = False
#                                     balance_offer.balance = balance_offer.balans - (
#                                             (offer_1.total_price_is_offer / offer_1.quantity) * offer.quantity)
#                                     balance_offer_sell.balance = balance_offer_sell.balans + (
#                                             (offer_1.total_price_is_offer / offer_1.quantity) * offer.quantity)
#                                     inventory_offer.quantity += offer.quantity
#                                     inventory_offer_sell.quantity -= offer.quantity
#                                     offer_1.quantity -= offer.quantity
#                                     offer.quantity -= offer.quantity
#                                     balance_offer_sell.save()
#                                     balance_offer.save()
#                                     inventory_offer.save()
#                                     inventory_offer_sell.save()
#                                     offer_1.save()
#                                     offer.save()
#                                 elif offer.quantity == offer_1.quantity:
#                                     balance_offer.balance -= offer_1.total_price_is_offer
#                                     balance_offer_sell.balance += offer_1.total_price_is_offer
#                                     offer_1.is_activate = False
#                                     offer.is_activate = False
#                                     inventory_offer_sell.quantity -= offer.quantity
#                                     inventory_offer.quantity += offer_1.quantity
#                                     offer.quantity -= offer.quantity
#                                     offer_1.quantity -= offer_1.quantity
#                                     balance_offer_sell.save()
#                                     balance_offer.save()
#                                     inventory_offer_sell.save()
#                                     inventory_offer.save()
#                                     offer_1.save()
#                                     offer.save()
#                     else:
#                         continue
#                 elif offer.quantity < offer_sell.quantity:
#                     offer.is_activate = False
#                     balance_offer.balance = balance_offer.balans - ((offer_sell.total_price_is_offer
#                                                                      / offer_sell.quantity) * offer.quantity)
#                     balance_offer_sell.balance = balance_offer_sell.balans + ((offer_sell.total_price_is_offer /
#                                                                                offer_sell.quantity) * offer.quantity)
#                     inventory_offer.quantity += offer.quantity
#                     inventory_offer_sell.quantity -= offer.quantity
#                     offer_sell.quantity -= offer.quantity
#                     offer.quantity -= offer.quantity
#                     balance_offer_sell.save()
#                     balance_offer.save()
#                     inventory_offer.save()
#                     inventory_offer_sell.save()
#                     offer_sell.save()
#                     offer.save()
#                 elif offer.quantity == offer_sell.quantity:
#                     balance_offer.balance -= offer_sell.total_price_is_offer
#                     balance_offer_sell.balance += offer_sell.total_price_is_offer
#                     offer_sell.is_activate = False
#                     offer.is_activate = False
#                     inventory_offer_sell.quantity -= offer.quantity
#                     inventory_offer.quantity += offer_sell.quantity
#                     offer.quantity -= offer.quantity
#                     offer_sell.quantity -= offer_sell.quantity
#                     balance_offer_sell.save()
#                     balance_offer.save()
#                     inventory_offer_sell.save()
#                     inventory_offer.save()
#                     offer_sell.save()
#                     offer.save()
#             else:
#                 continue
#     else:
#         print("offers are over")