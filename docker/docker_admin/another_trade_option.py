#
# class Trading:
#     @classmethod
#     def looks_for_seller_for_buyers_and_make_trade_(cls):
#         list_offer_buyer = list(Offer.objects.filter(type_function=1, is_activate=True))
#         if list_offer_buyer:
#             for offer_buy in list_offer_buyer:
#                 list_offer_seller = list(
#                     Offer.objects.filter(type_function=2, is_activate=True, price__gte=offer_buy.price))
#                 the_first_offer_seller = list_offer_seller[0]
#                 balance_offer_buy = list(Balance.objects.filter(user=offer_buy.user))
#                 balance_offer_buy = balance_offer_buy[0]
#                 balance_offer_sell = list(Balance.objects.filter(user=the_first_offer_seller.user))
#                 balance_offer_sell = balance_offer_sell[0]
#                 inventory_offer = list(Inventory.objects.filter(user=offer_buy.user))
#                 inventory_offer = inventory_offer[0]
#                 inventory_offer_sell = list(Inventory.objects.filter(user=the_first_offer_seller.user))
#                 inventory_offer_sell = inventory_offer_sell[0]
#                 if the_first_offer_seller and balance_offer_buy.balance > the_first_offer_seller.total_price_is_offer:
#                     Trade.objects.create(client=offer_buy.user, client_offer=offer_buy.offer,
#                                          quantity_client=offer_buy.quantity,
#                                          price_total=offer_buy.total_price_is_offer,
#                                          seller=the_first_offer_seller.user,
#                                          seller_offer=the_first_offer_seller,
#                                          quantity_seller=the_first_offer_seller.quantity,
#                                          price_total_1=the_first_offer_seller.total_price_is_offer)
#
#                     return cls.if_the_buyer_more_and_if_seller_more_and_the_buyer_and_the_seller_have_equal(
#                         offer_buy=offer_buy, the_first_offer_seller=the_first_offer_seller,
#                         balance_offer_buy=balance_offer_buy,
#                         balance_offer_sell=balance_offer_sell, inventory_offer=inventory_offer,
#                         inventory_offer_sell=inventory_offer_sell
#                     )
#                 else:
#                     continue
#
#     @classmethod
#     def if_the_buyer_has_more(cls, balance_offer_buy, balance_offer_sell, inventory_offer, inventory_offer_sell,
#                               the_first_offer_seller, offer_buy):
#         balance_offer_buy.balance -= the_first_offer_seller.total_price_is_offer
#         balance_offer_sell.balance += the_first_offer_seller.total_price_is_offer
#         offer_buy.quantity -= the_first_offer_seller.quantity
#         the_first_offer_seller.quantity -= the_first_offer_seller.quantity
#         inventory_offer.quantity += the_first_offer_seller.quantity
#         inventory_offer_sell.quantity -= the_first_offer_seller.quantity
#         the_first_offer_seller.is_activate = False
#         the_first_offer_seller.save()
#         offer_buy.save()
#         balance_offer_sell.save()
#         balance_offer_buy.save()
#         inventory_offer_sell.save()
#         inventory_offer.save()
#         if offer_buy.is_activate:
#             return cls.if_the_first_offer_do_not_covers_the_first_offer_of_seller(offer_buy=offer_buy,
#                                                                                   the_first_offer_seller
#                                                                                   =the_first_offer_seller
#                                                                                   )
#         return offer_buy, the_first_offer_seller
#
#     @classmethod
#     def if_the_first_offer_do_not_covers_the_first_offer_of_seller(cls, offer_buy, the_first_offer_seller):
#
#         for offer_sell_if_the_first_offer_sell_not_covers in the_first_offer_seller:
#             balance_offer_sell = list(Balance.objects.filter(user=offer_sell_if_the_first_offer_sell_not_covers.user))
#             balance_offer_sell = balance_offer_sell[0]
#             balance_offer = list(Balance.objects.filter(user=offer_buy.user))
#             balance_offer = balance_offer[0]
#             inventory_offer_sell = list(
#                 Inventory.objects.filter(user=offer_sell_if_the_first_offer_sell_not_covers.user))
#             inventory_offer_sell = inventory_offer_sell[0]
#             inventory_offer = list(Inventory.objects.filter(user=offer_buy.user))
#             inventory_offer = inventory_offer[0]
#             if not offer_sell_if_the_first_offer_sell_not_covers or not offer_buy.is_activate:
#                 Trade.objects.create(client=offer_buy.user, client_offer=offer_buy,
#                                      quantity_client=offer_buy.quantity,
#                                      price_total=offer_buy.total_price_is_offer,
#                                      seller=offer_sell_if_the_first_offer_sell_not_covers.user,
#                                      seller_offer=offer_sell_if_the_first_offer_sell_not_covers,
#                                      quantity_seller=offer_sell_if_the_first_offer_sell_not_covers.quantity,
#                                      price_total_1=offer_sell_if_the_first_offer_sell_not_covers.total_price_is_offer)
#                 return cls.if_the_offer_1_has_more_and_the_offer_buy_has_more_and_offer_1_and_offer_buy_have_equal(
#                     offer_sell_if_the_first_offer_sell_not_covers=offer_sell_if_the_first_offer_sell_not_covers,
#                     balance_offer=balance_offer, balance_offer_sell=balance_offer_sell,
#                     inventory_offer=inventory_offer, inventory_offer_sell=inventory_offer_sell, offer_buy=offer_buy)
#
#     @classmethod
#     def the_offer_buy_has_more(cls, offer_sell_if_the_first_offer_sell_not_covers, offer_buy, balance_offer_sell,
#                                balance_offer,
#                                inventory_offer_sell,
#                                inventory_offer):
#         offer_sell_if_the_first_offer_sell_not_covers.is_activate = False
#         balance_offer.balance -= offer_sell_if_the_first_offer_sell_not_covers.total_price_is_offer
#         balance_offer_sell.balance += offer_sell_if_the_first_offer_sell_not_covers.total_price_is_offer
#         inventory_offer.quantity += offer_sell_if_the_first_offer_sell_not_covers.quantity
#         inventory_offer_sell.quantity -= offer_sell_if_the_first_offer_sell_not_covers.quantity
#         offer_buy.quantity -= offer_sell_if_the_first_offer_sell_not_covers.quantity
#         offer_sell_if_the_first_offer_sell_not_covers.quantity -= offer_sell_if_the_first_offer_sell_not_covers.quantity
#         balance_offer_sell.save()
#         balance_offer.save()
#         inventory_offer_sell.save()
#         inventory_offer.save()
#         offer_sell_if_the_first_offer_sell_not_covers.save()
#         offer_buy.save()
#         return offer_buy, offer_sell_if_the_first_offer_sell_not_covers
#
#     @classmethod
#     def the_offer_1_has_more(cls, offer_sell_if_the_first_offer_sell_not_covers, offer_buy, balance_offer,
#                              balance_offer_sell,
#                              inventory_offer,
#                              inventory_offer_sell):
#         offer_buy.is_activate = False
#         balance_offer.balance = balance_offer.balans - (
#                 (
#                         offer_sell_if_the_first_offer_sell_not_covers.total_price_is_offer /
#                         offer_sell_if_the_first_offer_sell_not_covers.quantity) * offer_buy.quantity)
#         balance_offer_sell.balance = balance_offer_sell.balans + (
#                 (
#                         offer_sell_if_the_first_offer_sell_not_covers.total_price_is_offer /
#                         offer_sell_if_the_first_offer_sell_not_covers.quantity) * offer_buy.quantity)
#         inventory_offer.quantity += offer_buy.quantity
#         inventory_offer_sell.quantity -= offer_buy.quantity
#         offer_sell_if_the_first_offer_sell_not_covers.quantity -= offer_buy.quantity
#         offer_buy.quantity -= offer_buy.quantity
#         balance_offer_sell.save()
#         balance_offer.save()
#         inventory_offer.save()
#         inventory_offer_sell.save()
#         offer_sell_if_the_first_offer_sell_not_covers.save()
#         offer_buy.save()
#         return offer_buy, offer_sell_if_the_first_offer_sell_not_covers
#
#     @classmethod
#     def the_offer_1_and_offer_buy_have_equal(cls, offer_sell_if_the_first_offer_sell_not_covers, offer_buy,
#                                              balance_offer,
#                                              inventory_offer, inventory_offer_sell, balance_offer_sell, ):
#         balance_offer.balance -= offer_sell_if_the_first_offer_sell_not_covers.total_price_is_offer
#         balance_offer_sell.balance += offer_sell_if_the_first_offer_sell_not_covers.total_price_is_offer
#         offer_sell_if_the_first_offer_sell_not_covers.is_activate = False
#         offer_buy.is_activate = False
#         inventory_offer_sell.quantity -= offer_buy.quantity
#         inventory_offer.quantity += offer_sell_if_the_first_offer_sell_not_covers.quantity
#         offer_buy.quantity -= offer_buy.quantity
#         offer_sell_if_the_first_offer_sell_not_covers.quantity -= offer_sell_if_the_first_offer_sell_not_covers.quantity
#         balance_offer_sell.save()
#         balance_offer.save()
#         inventory_offer_sell.save()
#         inventory_offer.save()
#         offer_sell_if_the_first_offer_sell_not_covers.save()
#         offer_buy.save()
#         return offer_buy, offer_sell_if_the_first_offer_sell_not_covers
#
#     @classmethod
#     def if_the_offer_1_has_more_and_the_offer_buy_has_more_and_offer_1_and_offer_buy_have_equal(cls,
#                                                                                                 offer_sell_if_the_first_offer_sell_not_covers,
#                                                                                                 offer_buy,
#                                                                                                 balance_offer,
#                                                                                                 balance_offer_sell,
#                                                                                                 inventory_offer,
#                                                                                                 inventory_offer_sell):
#         if offer_buy.quantity > offer_sell_if_the_first_offer_sell_not_covers.quantity:
#             return cls.the_offer_buy_has_more(
#                 offer_sell_if_the_first_offer_sell_not_covers=offer_sell_if_the_first_offer_sell_not_covers,
#                 offer_buy=offer_buy,
#                 balance_offer_sell=balance_offer_sell, inventory_offer=inventory_offer,
#                 inventory_offer_sell=inventory_offer_sell, balance_offer=balance_offer)
#         elif offer_buy.quantity < offer_sell_if_the_first_offer_sell_not_covers.quantity:
#             return cls.the_offer_1_has_more(
#                 offer_sell_if_the_first_offer_sell_not_covers=offer_sell_if_the_first_offer_sell_not_covers,
#                 offer_buy=offer_buy,
#                 balance_offer_sell=balance_offer_sell, inventory_offer=inventory_offer,
#                 inventory_offer_sell=inventory_offer_sell, balance_offer=balance_offer)
#         elif offer_buy.quantity == offer_sell_if_the_first_offer_sell_not_covers.quantity:
#             return cls.the_offer_1_and_offer_buy_have_equal(
#                 offer_sell_if_the_first_offer_sell_not_covers=offer_sell_if_the_first_offer_sell_not_covers,
#                 offer_buy=offer_buy,
#                 balance_offer_sell=balance_offer_sell,
#                 inventory_offer=inventory_offer,
#                 inventory_offer_sell=inventory_offer_sell,
#                 balance_offer=balance_offer)
#
#     @classmethod
#     def the_buyer_and_seller_have_equal(cls, offer_buy, the_first_offer_seller, balance_offer_buy, balance_offer_sell,
#                                         inventory_offer, inventory_offer_sell):
#
#         offer_buy.quantity -= offer_buy.quantity
#         the_first_offer_seller.quantity -= the_first_offer_seller.quantity
#         inventory_offer.quantity -= offer_buy.quantity
#         inventory_offer_sell.quantity -= the_first_offer_seller.quantity
#         balance_offer_buy.balance -= the_first_offer_seller.total_price_is_offer
#         balance_offer_sell.balance -= the_first_offer_seller.total_price_is_offer
#         the_first_offer_seller.is_activate = False
#         offer_buy.is_activate = False
#         offer_buy.save()
#         the_first_offer_seller.save()
#         inventory_offer.save()
#         inventory_offer_sell.save()
#         balance_offer_sell.save()
#         balance_offer_buy.save()
#         return offer_buy, the_first_offer_seller
#
#     @classmethod
#     def the_seller_has_more(cls, offer_buy, the_first_offer_seller, balance_offer_buy, balance_offer_sell,
#                             inventory_offer, inventory_offer_sell):
#         the_first_offer_seller.quantity -= offer_buy.quantity
#         offer_buy.quantity -= offer_buy.quantity
#         inventory_offer.quantity += offer_buy.quantity
#         inventory_offer_sell.quantity -= the_first_offer_seller.quantity
#         balance_offer_buy.balance -= \
#             (the_first_offer_seller.total_price_is_offer /
#              the_first_offer_seller.quantity) * offer_buy.quantity
#         balance_offer_sell.balance += (
#                                               the_first_offer_seller.total_price_is_offer /
#                                               the_first_offer_seller.quantity) * offer_buy.quantity
#         the_first_offer_seller.is_activate = False
#         offer_buy.save()
#         offer_buy.save()
#         balance_offer_sell.save()
#         balance_offer_buy.save()
#         inventory_offer.save()
#         inventory_offer_sell.save()
#         return offer_buy, the_first_offer_seller
#
#     @classmethod
#     def if_the_buyer_more_and_if_seller_more_and_the_buyer_and_the_seller_have_equal(cls, offer_buy,
#                                                                                      the_first_offer_seller,
#                                                                                      balance_offer_buy,
#                                                                                      balance_offer_sell,
#                                                                                      inventory_offer,
#                                                                                      inventory_offer_sell):
#         if offer_buy.quantity > the_first_offer_seller.quantity:
#             return cls.if_the_buyer_has_more(offer_buy=offer_buy, the_first_offer_seller=the_first_offer_seller,
#                                              balance_offer_sell=balance_offer_sell, balance_offer_buy=balance_offer_buy,
#                                              inventory_offer=inventory_offer, inventory_offer_sell=inventory_offer_sell)
#         elif offer_buy.quantity < the_first_offer_seller.quantity:
#             return cls.the_seller_has_more(offer_buy=offer_buy, the_first_offer_seller=the_first_offer_seller,
#                                            balance_offer_sell=balance_offer_sell, balance_offer_buy=balance_offer_buy,
#                                            inventory_offer=inventory_offer, inventory_offer_sell=inventory_offer_sell)
#         elif offer_buy.quantity == the_first_offer_seller.quantity:
#             return cls.the_buyer_and_seller_have_equal(offer_buy=offer_buy,
#                                                        the_first_offer_seller=the_first_offer_seller,
#                                                        balance_offer_sell=balance_offer_sell,
#                                                        balance_offer_buy=balance_offer_buy,
#                                                        inventory_offer=inventory_offer,
#                                                        inventory_offer_sell=inventory_offer_sell)
