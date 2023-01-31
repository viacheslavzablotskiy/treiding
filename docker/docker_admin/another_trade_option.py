class Make_trades:
    @classmethod
    def looks_for_seller_for_buyers_and_make_trade_(cls):
        from docker_admin.models import Offer
        offer_buy_offer = list(Offer.objects.filter(type_function=1, is_activate=True))
        offer_is_buy = offer_buy_offer
        if offer_is_buy:
            for offer_buy in offer_is_buy:
                cls.make_trade_(offer_buy=offer_buy)
                offer_seller = list(Offer.objects.filter(type_function=2, is_activate=True, price__gte=offer_buy.price))
                if offer_seller:
                    offer_seller = offer_seller[0]
                    cls.make_trade_(offer_seller=offer_seller)
                    return cls.make_trade_(offer_buy=offer_buy, offer_seller=offer_seller)

    @classmethod
    def make_trade_(cls, offer_buy, offer_seller):
        from docker_admin.models import Trade
        Trade.objects.create(client=offer_buy.user, client_offer=offer_buy.offer,
                             quantity_client=offer_buy.quantity,
                             price_total=offer_buy.total_price_is_offer,
                             seller=offer_seller.user,
                             seller_offer=offer_seller,
                             quantity_seller=offer_seller.quantity,
                             price_total_1=offer_seller.total_price_is_offer)
        cls.balance_and_inventory(offer_buy=offer_buy)
        cls.balance_and_inventory(offer_seller=offer_seller)

    @classmethod
    def balance_and_inventory(cls, offer_buy, offer_seller):
        from docker_admin.models import Balance, Inventory
        balance_offer_buy = list(Balance.objects.filter(user=offer_buy.user))
        balance_offer_buy = balance_offer_buy[0]
        cls.if_the_buyer_has_more(balance_offer_buy=balance_offer_buy)
        balance_offer_sell = list(Balance.objects.filter(user=offer_seller.user))
        balance_offer_sell = balance_offer_sell[0]
        cls.if_the_buyer_has_more(balance_offer_sell=balance_offer_sell)
        inventory_offer = list(Inventory.objects.filter(user=offer_buy.user))
        inventory_offer = inventory_offer[0]
        cls.if_the_buyer_has_more(inventory_offer=inventory_offer)
        inventory_offer_sell = list(Inventory.objects.filter(user=offer_seller.user))
        inventory_offer_sell = inventory_offer_sell[0]
        cls.if_the_buyer_has_more(inventory_offer_sell=inventory_offer_sell)
        cls.if_the_buyer_has_more(offer_buy=offer_buy)
        cls.if_the_buyer_has_more(offer_seller=offer_seller)
        return offer_buy, offer_seller

    @classmethod
    def the_seller_has_more(cls, offer_buy, offer_seller, balance_offer_buy, balance_offer_sell,
                            inventory_offer, inventory_offer_sell):
        offer_seller.quantity -= offer_buy.quantity
        offer_buy.quantity -= offer_buy.quantity
        inventory_offer.quantity += offer_buy.quantity
        inventory_offer_sell.quantity -= offer_seller.quantity
        balance_offer_buy.balance -= (offer_seller.total_price_is_offer / offer_seller.quantity) * offer_buy.quantity
        balance_offer_sell.balance += (offer_seller.total_price_is_offer / offer_seller.quantity) * offer_buy.quantity
        offer_seller.is_activate = False
        offer_buy.save()
        offer_buy.save()
        balance_offer_sell.save()
        balance_offer_buy.save()
        inventory_offer.save()
        inventory_offer_sell.save()
        cls.the_buyer_and_seller_have_equal(balance_offer_buy=balance_offer_buy, offer_seller=offer_seller,
                                            offer_buy=offer_buy,
                                            balance_offer_sell=balance_offer_sell, inventory_offer=inventory_offer,
                                            inventory_offer_sell=inventory_offer_sell)
        return offer_buy, offer_seller

    @classmethod
    def the_buyer_and_seller_have_equal(cls, offer_buy, offer_seller, balance_offer_buy, balance_offer_sell,
                                        inventory_offer, inventory_offer_sell):

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
        cls.if_the_buyer_more_and_if_seller_more_and_the_buyer_and_the_seller_have_equal(offer_seller=offer_seller)
        cls.if_the_buyer_more_and_if_seller_more_and_the_buyer_and_the_seller_have_equal(offer_buy=offer_buy)
        return offer_buy, offer_seller

    @classmethod
    def if_the_buyer_more_and_if_seller_more_and_the_buyer_and_the_seller_have_equal(cls, offer_buy, offer_seller):
        if offer_buy.quantity > offer_seller.quantity:
            return cls.if_the_buyer_has_more(offer_buy, offer_seller)
        elif offer_buy.quantity < offer_seller.quantity:
            return cls.the_seller_has_more(offer_buy, offer_seller)
        elif offer_buy.quantity == offer_seller.quantity:
            return cls.the_buyer_and_seller_have_equal(offer_buy, offer_seller)
        return offer_buy, offer_seller

    @classmethod
    def if_the_buyer_has_more(cls, balance_offer_buy, balance_offer_sell, inventory_offer, inventory_offer_sell,
                              offer_seller, offer_buy):
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
        cls.the_seller_has_more(balance_offer_buy=balance_offer_buy, offer_seller=offer_seller, offer_buy=offer_buy,
                                balance_offer_sell=balance_offer_sell, inventory_offer=inventory_offer,
                                inventory_offer_sell=inventory_offer_sell)
        cls.if_the_first_offer_do_not_covers_the_first_offer_of_seller(offer_buy=offer_buy, offer_seller = offer_seller)
        cls.my_trade(offer_seller=offer_seller, offer_buy=offer_buy)
        if offer_buy.is_activate:
            return cls.if_the_first_offer_do_not_covers_the_first_offer_of_seller(offer_buy
            )
        return offer_buy, offer_seller


    @classmethod
    def my_trade(cls, offer_buy, offer_seller):
        cls.make_trade_(offer_seller, offer_buy

                        )
        cls.balance_and_inventory(offer_seller, offer_buy

                                  )
        cls.if_the_buyer_more_and_if_seller_more_and_the_buyer_and_the_seller_have_equal(
            offer_seller, offer_buy
        )
        return offer_seller, offer_buy

    @classmethod
    def if_the_first_offer_do_not_covers_the_first_offer_of_seller(cls, offer_buy, offer_seller):
        from docker_admin.models import Offer, Trade
        offer_seller = list(Offer.objects.filter(type_function=2, price__gte=offer_buy.price, is_activate=True))
        for offer_1 in offer_seller:
            if not offer_1 or not offer_buy.is_activate:
                Trade.objects.create(client=offer_buy.user, client_offer=offer_buy,
                                     quantity_client=offer_buy.quantity,
                                     price_total=offer_buy.total_price_is_offer, seller=offer_1.user,
                                     seller_offer=offer_1,
                                     quantity_seller=offer_1.quantity,
                                     price_total_1=offer_1.total_price_is_offer)
                cls.balance_and_inventory_in_the_function_if_the_buyer_has_more(offer_buy=offer_buy)
                cls.balance_and_inventory_in_the_function_if_the_buyer_has_more(offer_1=offer_1)
                cls.make_trade_if_do_not_covers_the_first_offer_of_seller(offer_seller=offer_seller)
                cls.make_trade_if_do_not_covers_the_first_offer_of_seller(offer_buy=offer_buy)
            return cls.if_the_offer_1_has_more_and_the_offer_buy_has_more_and_offer_1_and_offer_buy_have_equal(offer_1,
                                                                                                               offer_buy)
        return offer_buy

    @classmethod
    def balance_and_inventory_in_the_function_if_the_buyer_has_more(cls, offer_buy, offer_1):
        from docker_admin.models import Inventory, Balance
        inventory_offer = list(Inventory.objects.filter(user=offer_buy.user))
        inventory_offer = inventory_offer[0]
        cls.the_offer_buy_has_more(inventory_offer=inventory_offer)
        inventory_offer_sell = list(Inventory.objects.filter(user=offer_1.user))
        inventory_offer_sell = inventory_offer_sell[0]
        cls.the_offer_buy_has_more(inventory_offer_sell=inventory_offer_sell)
        balance_offer = list(Balance.objects.filter(user=offer_buy.user))
        balance_offer = balance_offer[0]
        cls.the_offer_buy_has_more(balance_offer=balance_offer)
        balance_offer_sell = list(Balance.objects.filter(user=offer_1.user))
        balance_offer_sell = balance_offer_sell[0]
        cls.the_offer_buy_has_more(balance_offer_sell=balance_offer_sell)
        cls.the_offer_buy_has_more(offer_1=offer_1)
        cls.the_offer_buy_has_more(offer_buy=offer_buy)

    @classmethod
    def the_offer_buy_has_more(cls, offer_1, offer_buy, balance_offer_sell, balance_offer, inventory_offer_sell,
                               inventory_offer):
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
        cls.the_offer_1_has_more(offer_1=offer_1, offer_buy=offer_buy, balance_offer_sell=balance_offer_sell,
                                 balance_offer=balance_offer, inventory_offer=inventory_offer,
                                 inventory_offer_sell=inventory_offer_sell)
        return offer_buy, offer_1

    @classmethod
    def the_offer_1_has_more(cls, offer_1, offer_buy, balance_offer, balance_offer_sell, inventory_offer,
                             inventory_offer_sell):
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
        cls.the_offer_1_and_offer_buy_have_equal(offer_1=offer_1, offer_buy=offer_buy,
                                                 balance_offer_sell=balance_offer_sell,
                                                 balance_offer=balance_offer, inventory_offer=inventory_offer,
                                                 inventory_offer_sell=inventory_offer_sell)
        return offer_buy, offer_1

    @classmethod
    def the_offer_1_and_offer_buy_have_equal(cls, offer_1, offer_buy, balance_offer, balance_offer_sell,
                                             inventory_offer, inventory_offer_sell):
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
        cls.make_trade_if_do_not_covers_the_first_offer_of_seller(
            offer_1=offer_1, offer_buy=offer_buy,
            balance_offer_sell=balance_offer_sell,
            balance_offer=balance_offer,
            inventory_offer=inventory_offer,
            inventory_offer_sell=inventory_offer_sell)
        cls.if_the_offer_1_has_more_and_the_offer_buy_has_more_and_offer_1_and_offer_buy_have_equal(
            offer_1=offer_1,
            offer_buy=offer_buy,
            balance_offer_sell=balance_offer_sell,
            balance_offer=balance_offer,
            inventory_offer=inventory_offer,
            inventory_offer_sell=inventory_offer_sell)
        return offer_buy, offer_1

    @classmethod
    def if_the_offer_1_has_more_and_the_offer_buy_has_more_and_offer_1_and_offer_buy_have_equal(cls, offer_1,
        offer_buy, balance_offer, balance_offer_sell, inventory_offer, inventory_offer_sell):
        if offer_buy.quantity > offer_1.quantity:
            return cls.the_offer_buy_has_more(offer_1, offer_buy)
        elif offer_buy.quantity < offer_1.quantity:
            return cls.the_offer_1_has_more(offer_1, offer_buy)
        elif offer_buy.quantity == offer_1.quantity:
            return cls.the_offer_1_and_offer_buy_have_equal(offer_1, offer_buy)
        cls.if_the_offer_1_has_more_and_the_offer_buy_has_more_and_offer_1_and_offer_buy_have_equal(
            offer_1=offer_1)

    @classmethod
    def make_trade_if_do_not_covers_the_first_offer_of_seller(cls, offer_1, offer_buy, balance_offer,
                                                              balance_offer_sell, inventory_offer,
                                                              inventory_offer_sell, offer_seller):
        cls.if_the_first_offer_do_not_covers_the_first_offer_of_seller(offer_seller)
        cls.if_the_offer_1_has_more_and_the_offer_buy_has_more_and_offer_1_and_offer_buy_have_equal(offer_1,
                                                                                                    offer_buy)




