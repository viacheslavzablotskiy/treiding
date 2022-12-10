from django.db import models
from django.contrib.auth.models import User


class CodeName(models.Model):
    code = models.CharField(max_length=255,  null=True, unique=True)
    name = models.CharField(max_length=255,  null=True, unique=True)

    def __str__(self):
        return f'{self.name}:{self.code}'


class Currency(models.Model):
    valuta = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return f'{self.valuta}'


class Item(models.Model):
    name = models.ForeignKey('CodeName', max_length=255, blank=True, null=True, on_delete = models.SET_NULL)
    valuta = models.ForeignKey('Currency', blank=True, null=True, on_delete=models.CASCADE)
    price = models.ForeignKey('Price', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'


class Price(models.Model):
    price = models.DecimalField(max_digits=5, decimal_places=2, max_length=5, null=True, blank=True)

    def __str__(self):
        return f'{self.price}'


class WatchList(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey("Item", blank=True, null=True, on_delete=models.SET_NULL)
    is_publishid = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.item}'


class Offer(models.Model):
    RATE_CHOICES = (
        (1, 'BUY'),
        (2, 'ADD'),
    )
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    item = models.ForeignKey("Item", blank=True, null=True, on_delete=models.CASCADE)
    price = models.ForeignKey('Price', null=True, blank=True,  on_delete=models.SET_NULL, related_name="priceprice",
                              related_query_name="priceprice")
    is_active = models.BooleanField(default=True)
    quantity = models.IntegerField(blank=True, null=True)
    type_function = models.PositiveIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return f'{self.item}'


class Balans(models.Model):
    balans = models.DecimalField(max_digits=5, decimal_places=2, max_length=5, null=True, blank=True)

    def __str__(self):
        return f"{self.balans}"


class Trade(models.Model):
    client = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="client_trade",
                               related_query_name="client_trade")
    seller = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="seller_trade",
                               related_query_name="seller_trade")
    item = models.ForeignKey('Item', blank=True, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(blank=True, null=True, )
    price_dena = models.DecimalField(max_digits=5, decimal_places=2,  max_length=5)
    description = models.TextField(max_length=255, blank=True, null=True)
    client_offer = models.ForeignKey('Offer', blank=True, null=True, on_delete=models.SET_NULL,
                                     related_name='client_offer_trade',
                                     related_query_name="client_offer_trade")
    seller_offer = models.ForeignKey('Offer', blank=True, null=True, on_delete=models.SET_NULL,
                                     related_name="seller_offer_trade",
                                     related_query_name="seller_offer_trade")

    def __str__(self):
        return f'{self.item}'


class Inventory(models.Model):
    item = models.ForeignKey('Item', blank=True, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.ForeignKey('Price', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.item}'
