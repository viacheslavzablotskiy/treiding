from itertools import count

from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver




class CodeName(models.Model):
    code = models.CharField(max_length=255, null=True, unique=True)
    name = models.CharField(max_length=255, null=True, unique=True)

    def __str__(self):
        return f'{self.name}:{self.code}'


class Currency(models.Model):
    valuta = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return f'{self.valuta}'


class Item(models.Model):
    name = models.ForeignKey('CodeName', max_length=255, blank=True, null=True, on_delete=models.SET_NULL)
    valuta = models.ForeignKey('Currency', blank=True, null=True, on_delete=models.CASCADE)
    max_price = models.DecimalField(max_digits=5, decimal_places=2, max_length=5, null=True, blank=True)
    # price = models.ForeignKey('Price', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} + {self.valuta}'


    # def save(self, *args, **kwargs):
    #     price_item = 4
    #     price_item_1 = 8
    #     if self.price >= 25.00:
    #         self.price -= price_item
    #     else:
    #         self.price -= price_item_1
    #
    #     price_item_item = self.price
    #     self.total_price_item = self.total_price * price_item_item
    #     super(Price, self).save(*args, **kwargs)


    # @receiver(post_save, sender=Price)
    # def price_price(sender, instance, *args, **kwargs):
    #     price_item = instance.price
    #     instance.price_item_price = instance.total_price * price_item
    #     instance.price_item_price.save()
    # def discount(self, discount: float = 3.00) -> str:
    #     if self.price > 25.00:
    #         return f'{self.price - discount}'

    # def discount(self, discount: float = 0.012) -> str:
    #     return f'{(float(self.price) / discount)}'


class WatchList(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey("Item", blank=True, null=True, on_delete=models.SET_NULL)
    is_publishid = models.BooleanField(default=True)


    def __str__(self):
        return f'{self.item} + {self.user}+ {self.is_publishid}'


class Offer(models.Model):
    RATE_CHOICES = (
        (1, 'BUY'),
        (2, 'ADD'),
    )
    user = models.ForeignKey('auth.User',  null=True,  on_delete=models.CASCADE)
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.CASCADE)
    total_price_is_offer = models.DecimalField(max_digits=5, decimal_places=2, max_length=5, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    type_function = models.PositiveIntegerField(choices=RATE_CHOICES, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, max_length=5, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.total_price_is_offer = self.quantity * self.price
        super(Offer, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.item} + {self.item}+ {self.total_price_is_offer}+{self.quantity}+{self.type_function}+{self.price}'


class Balans(models.Model):
    user = models.ForeignKey("auth.User", null=True, blank=True, on_delete=models.SET_NULL)
    balans = models.DecimalField(max_digits=5, decimal_places=2, max_length=5, null=True, blank=True, default=400)

    def __str__(self):
        return f"{self.balans} + {self.balans}"

    @receiver(post_save, sender=User)
    def create_user_balans(sender, instance, created, **kwargs):
        if created:
            Balans.objects.create(user=instance, balans=0)





class Trade(models.Model):
    client = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="client_trade",
                               related_query_name="client_trade")
    client_offer = models.ForeignKey('Offer', blank=True, null=True, on_delete=models.SET_NULL,
                                     related_name='client_offer_trade',
                                     related_query_name="client_offer_trade")
    quantity_client = models.DecimalField(max_digits=5, decimal_places=2, max_length=5, null=True, blank=True, default=400)
    price_total = models.DecimalField(max_digits=5, decimal_places=2, max_length=5,null=True, blank=True)

    seller = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="seller_trade",
                               related_query_name="seller_trade")
    seller_offer = models.ForeignKey('Offer', blank=True, null=True, on_delete=models.SET_NULL,
                                     related_name="seller_offer_trade",
                                     related_query_name="seller_offer_trade")
    quantity_seller = models.DecimalField(max_digits=5, decimal_places=2, max_length=5, null=True, blank=True, default=400)
    price_total_1 = models.DecimalField(max_digits=5, decimal_places=2, max_length=5, null=True, blank=True)

    def __str__(self):
        return f'{self.client} +{self.client_offer}+{self.quantity_client}+{self.price_total}+{self.seller}+{self.seller_offer}+{self.quantity_seller}+{self.price_total_1} '



class Inventory(models.Model):
    user = models.ForeignKey('auth.User', null=True, blank=True,  on_delete=models.CASCADE)
    item_1 = models.ForeignKey('Item', blank=True, null=True, on_delete=models.CASCADE, related_name="item_name_2",
                               related_query_name="item_name_2")
    quantity = models.IntegerField(default=0)


    def __str__(self):
        return f'{self.user} + {self.quantity} + {self.item_1}'

    @receiver(post_save, sender=User)
    def create_user_balans(sender, instance, created, **kwargs):
        if created:
            Inventory.objects.create(user=instance, item_1=1, quantity=0)

    @receiver(post_save, sender=Trade)
    def create_user_balans(sender, instance, created, client_offer=None,  **kwargs):
        if created:
            Currency.objects.create(valuta="USD")






    # def save(self, *args, **kwargs):
    #     name_item = Item.objects.filter().count()
    #     self.quantity = name_item
    #     super(Inventory, self).save(*args, **kwargs)
