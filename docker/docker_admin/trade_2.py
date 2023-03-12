from docker_admin.models import *


class Trading:

    @classmethod
    def find_suitable_offer_sell_and_make_trade_(cls):
        list_offer_for_buyer = list(Offer.objects.filter(type_function=1, is_activate=True))
        if list_offer_for_buyer:
            for offer_buy in list_offer_for_buyer:
                list_offer_seller = list(
                    Offer.objects.filter(type_function=2, is_activate=True, is_locked=False,
                                         price__gte=offer_buy.price))
                first_offer_seller = list_offer_seller[0]
                balance_offer_buy = list(Balance.objects.filter(user=offer_buy.user))
                balance_offer_buy = balance_offer_buy[0]
                balance_offer_sell = list(Balance.objects.filter(user=first_offer_seller.user))
                balance_offer_sell = balance_offer_sell[0]
                inventory_offer_buy = list(Inventory.objects.filter(user=offer_buy.user))
                inventory_offer_buy = inventory_offer_buy[0]
                inventory_offer_sell = list(Inventory.objects.filter(user=first_offer_seller.user))
                inventory_offer_sell = inventory_offer_sell[0]
                if first_offer_seller and balance_offer_buy.balance > first_offer_seller.total_price_is_offer:
                    cls.make_trade_(offer_buy=offer_buy, first_offer_seller=first_offer_seller,
                                    balance_offer_sell=balance_offer_sell, balance_offer_buy=balance_offer_buy,
                                    inventory_offer_buy=inventory_offer_buy, inventory_offer_sell=inventory_offer_sell)
                else:
                    continue

    @classmethod
    def make_trade_(cls, offer_buy, inventory_offer_buy, inventory_offer_sell,
                    balance_offer_buy, balance_offer_sell, first_offer_seller):
        Trade.objects.create(client=offer_buy.user, client_offer=offer_buy.offer,
                             quantity_client=offer_buy.quantity,
                             price_total=offer_buy.total_price_is_offer,
                             seller=first_offer_seller.user,
                             seller_offer=first_offer_seller,
                             quantity_seller=first_offer_seller.quantity,
                             price_total_1=first_offer_seller.total_price_is_offer)
        cls.course_of_action(offer_buy=offer_buy,
                             first_offer_seller=first_offer_seller,
                             balance_offer_sell=balance_offer_sell,
                             balance_offer_buy=balance_offer_buy,
                             inventory_offer_buy=inventory_offer_buy,
                             inventory_offer_sell=inventory_offer_sell)

    @classmethod
    def if_offer_buy_has_more(cls, offer_buy, first_offer_seller, balance_offer_sell, balance_offer_buy,
                              inventory_offer_buy,
                              inventory_offer_sell):
        balance_offer_buy.balance -= first_offer_seller.total_price_is_offer
        balance_offer_sell.balance += first_offer_seller.total_price_is_offer
        offer_buy.quantity -= first_offer_seller.quantity
        first_offer_seller.quantity -= first_offer_seller.quantity
        inventory_offer_buy.quantity += first_offer_seller.quantity
        inventory_offer_sell.quantity -= first_offer_seller.quantity
        first_offer_seller.is_activate = False
        first_offer_seller.save()
        offer_buy.save()
        balance_offer_sell.save()
        balance_offer_buy.save()
        inventory_offer_sell.save()
        inventory_offer_buy.save()
        if offer_buy.is_activate:
            cls.if_the_first_offer_is_not_covered(offer_buy=offer_buy,
                                                  balance_offer_sell=balance_offer_sell,
                                                  balance_offer_buy=balance_offer_buy,
                                                  inventory_offer_buy=inventory_offer_buy,
                                                  inventory_offer_sell=inventory_offer_sell)

    @classmethod
    def if_the_first_offer_is_not_covered(cls, offer_buy, balance_offer_sell, balance_offer_buy,
                                          inventory_offer_buy, inventory_offer_sell):
        list_offer_seller = list(
            Offer.objects.filter(type_function=2, is_activate=True, is_locked=False,
                                 price__gte=offer_buy.price))
        for offer_sell in list_offer_seller:
            Trade.objects.create(client=offer_buy.user, client_offer=offer_buy, quantity_client=offer_buy.quantity,
                                 price_total=offer_buy.total_price_is_offer, seller=offer_sell.user,
                                 seller_offer=offer_sell, quantity_seller=offer_sell.quantity,
                                 price_total_1=offer_sell.total_price_is_offer)
            cls.course_of_action_offer_sell_(offer_sell=offer_sell, offer_buy=offer_buy,
                                             inventory_offer_sell=inventory_offer_sell,
                                             inventory_offer_buy=inventory_offer_buy,
                                             balance_offer_buy=balance_offer_buy,
                                             balance_offer_sell=balance_offer_sell, )

    @classmethod
    def the_offer_buy_has_more(cls, offer_sell, offer_buy, balance_offer_sell, balance_offer_buy, inventory_offer_sell,
                               inventory_offer_buy):
        balance_offer_buy.balance -= offer_sell.total_price_is_offer
        balance_offer_sell.balance += offer_sell.total_price_is_offer
        inventory_offer_buy.quantity += offer_sell.quantity
        inventory_offer_sell.quantity -= offer_sell.quantity
        offer_buy.quantity -= offer_sell.quantity
        offer_sell.quantity -= offer_sell.quantity
        offer_sell.is_activate = False
        balance_offer_sell.save()
        balance_offer_buy.save()
        inventory_offer_sell.save()
        inventory_offer_buy.save()
        offer_sell.save()
        offer_buy.save()

    @classmethod
    def the_offer_seller_has_more(cls, offer_sell, offer_buy, balance_offer_buy, balance_offer_sell,
                                  inventory_offer_buy, inventory_offer_sell):
        offer_sell.quantity -= offer_buy.quantity
        offer_buy.quantity -= offer_buy.quantity
        balance_offer_buy.balance = balance_offer_buy.balans - (
                (
                        offer_sell.total_price_is_offer /
                        offer_sell.quantity) * offer_buy.quantity)
        balance_offer_sell.balance = balance_offer_sell.balans + (
                (
                        offer_sell.total_price_is_offer /
                        offer_sell.quantity) * offer_buy.quantity)
        inventory_offer_buy.quantity += offer_buy.quantity
        inventory_offer_sell.quantity -= offer_buy.quantity
        offer_buy.is_activate = False
        balance_offer_sell.save()
        balance_offer_buy.save()
        inventory_offer_buy.save()
        inventory_offer_sell.save()
        offer_sell.save()
        offer_buy.save()

    @classmethod
    def both_quantity_equal(cls, offer_sell, offer_buy,
                            balance_offer_buy,
                            inventory_offer_buy, inventory_offer_sell, balance_offer_sell):
        balance_offer_buy.balance -= offer_sell.total_price_is_offer
        balance_offer_sell.balance += offer_sell.total_price_is_offer
        offer_sell.is_activate = False
        offer_buy.is_activate = False
        inventory_offer_sell.quantity -= offer_buy.quantity
        inventory_offer_buy.quantity += offer_sell.quantity
        offer_buy.quantity -= offer_buy.quantity
        offer_sell.quantity -= offer_sell.quantity
        balance_offer_sell.save()
        balance_offer_buy.save()
        inventory_offer_sell.save()
        inventory_offer_buy.save()
        offer_sell.save()
        offer_buy.save()

    @classmethod
    def course_of_action_offer_sell_(cls, offer_sell, offer_buy, balance_offer_buy, balance_offer_sell,
                                     inventory_offer_buy, inventory_offer_sell):
        if offer_buy.quantity > offer_sell.quantity:
            cls.the_offer_buy_has_more(
                offer_sell=offer_sell,
                offer_buy=offer_buy,
                balance_offer_sell=balance_offer_sell, inventory_offer_buy=inventory_offer_buy,
                inventory_offer_sell=inventory_offer_sell, balance_offer_buy=balance_offer_buy)
        elif offer_buy.quantity < offer_sell.quantity:
            cls.the_offer_seller_has_more(
                offer_sell=offer_sell,
                offer_buy=offer_buy,
                balance_offer_sell=balance_offer_sell, inventory_offer_buy=inventory_offer_buy,
                inventory_offer_sell=inventory_offer_sell, balance_offer_buy=balance_offer_buy)
        elif offer_buy.quantity == offer_sell.quantity:
            cls.both_quantity_equal(
                offer_sell=offer_sell,
                offer_buy=offer_buy,
                balance_offer_sell=balance_offer_sell,
                inventory_offer_buy=inventory_offer_buy,
                inventory_offer_sell=inventory_offer_sell,
                balance_offer_buy=balance_offer_buy)

    @classmethod
    def if_equal_quantity_(cls, offer_buy, first_offer_seller, balance_offer_buy, balance_offer_sell,
                           inventory_offer_buy, inventory_offer_sell):
        offer_buy.quantity -= offer_buy.quantity
        first_offer_seller.quantity -= first_offer_seller.quantity
        inventory_offer_buy.quantity -= offer_buy.quantity
        inventory_offer_sell.quantity -= first_offer_seller.quantity
        balance_offer_buy.balance -= first_offer_seller.total_price_is_offer
        balance_offer_sell.balance -= first_offer_seller.total_price_is_offer
        first_offer_seller.is_activate = False
        offer_buy.is_activate = False
        offer_buy.save()
        first_offer_seller.save()
        inventory_offer_buy.save()
        inventory_offer_sell.save()
        balance_offer_sell.save()
        balance_offer_buy.save()

    @classmethod
    def the_seller_has_more(cls, offer_buy, first_offer_seller, balance_offer_buy, balance_offer_sell,
                            inventory_offer_buy, inventory_offer_sell):
        first_offer_seller.quantity -= offer_buy.quantity
        offer_buy.quantity -= offer_buy.quantity
        inventory_offer_buy.quantity += offer_buy.quantity
        inventory_offer_sell.quantity -= first_offer_seller.quantity
        balance_offer_buy.balance -= \
            (first_offer_seller.total_price_is_offer /
             first_offer_seller.quantity) * offer_buy.quantity
        balance_offer_sell.balance += (
                                              first_offer_seller.total_price_is_offer /
                                              first_offer_seller.quantity) * offer_buy.quantity
        first_offer_seller.is_activate = False
        offer_buy.save()
        offer_buy.save()
        balance_offer_sell.save()
        balance_offer_buy.save()
        inventory_offer_buy.save()
        inventory_offer_sell.save()

    @classmethod
    def course_of_action(cls, offer_buy, first_offer_seller, balance_offer_buy, balance_offer_sell,
                         inventory_offer_buy,
                         inventory_offer_sell):
        if offer_buy.quantity > first_offer_seller.quantity:
            cls.if_offer_buy_has_more(offer_buy=offer_buy, first_offer_seller=first_offer_seller,
                                      balance_offer_sell=balance_offer_sell, balance_offer_buy=balance_offer_buy,
                                      inventory_offer_buy=inventory_offer_buy,
                                      inventory_offer_sell=inventory_offer_sell)
        elif offer_buy.quantity < first_offer_seller.quantity:
            cls.the_seller_has_more(offer_buy=offer_buy, first_offer_seller=first_offer_seller,
                                    balance_offer_sell=balance_offer_sell, balance_offer_buy=balance_offer_buy,
                                    inventory_offer_buy=inventory_offer_buy, inventory_offer_sell=inventory_offer_sell)
        elif offer_buy.quantity == first_offer_seller.quantity:
            cls.if_equal_quantity_(offer_buy=offer_buy,
                                   first_offer_seller=first_offer_seller,
                                   balance_offer_sell=balance_offer_sell,
                                   balance_offer_buy=balance_offer_buy,
                                   inventory_offer_buy=inventory_offer_buy,
                                   inventory_offer_sell=inventory_offer_sell)
