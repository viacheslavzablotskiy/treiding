from datetime import timedelta, datetime

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import User, PermissionsMixin
from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from docker_admin.tasks import send_verification_email
import uuid

from django.db import models
import uuid


class UserAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email address must be provided')

        if not password:
            raise ValueError('Password must be provided')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserAccountManager()

    email = models.EmailField('email', unique=True, blank=False, null=False)
    full_name = models.CharField('full name', blank=True, null=True, max_length=400)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
    is_verified = models.BooleanField('verified', default=False)  # Add the `is_verified` flag

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.email

    def __unicode__(self):
        return self.email


class CodeName(models.Model):
    code = models.CharField(max_length=255, null=True, unique=True)
    name = models.CharField(max_length=255, null=True, unique=True)

    def __str__(self):
        return f'{self.name}:{self.code}'

    def user_post_save(sender, instance, signal, *args, **kwargs):
        if not instance.is_verified:
            # Send verification email
            send_verification_email.delay(instance.pk)

    signals.post_save.connect(user_post_save, sender=User)

    def user_token_verified(sender, instance, signal, *args, **kwargs):
        if not instance.is_verified:
            Token.objects.create(user=instance)

    signals.post_save.connect(user_token_verified, sender=User)


class Currency(models.Model):
    valuta = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return f'{self.valuta}'


class Item(models.Model):
    name = models.ForeignKey('CodeName', max_length=255, blank=True, null=True, on_delete=models.SET_NULL)
    valuta = models.ForeignKey('Currency', blank=True, null=True, on_delete=models.CASCADE)
    max_price = models.DecimalField(max_digits=5, decimal_places=2, max_length=5, null=True, blank=True)

    def __str__(self):
        return f'{self.name} + {self.valuta}'


class WatchList(models.Model):
    user = models.ForeignKey(get_user_model(), blank=True, null=True, on_delete=models.SET_NULL, )
    item = models.ForeignKey("Item", blank=True, null=True, on_delete=models.SET_NULL)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.item} + {self.user}+ {self.is_published}'


class Offer(models.Model):
    RATE_CHOICES = (
        (1, 'BUY'),
        (2, 'ADD'),
    )
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.CASCADE)
    total_price_is_offer = models.DecimalField(max_digits=5, decimal_places=2, max_length=5, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    type_function = models.PositiveIntegerField(choices=RATE_CHOICES, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, max_length=5, null=True, blank=True)
    is_activate = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.total_price_is_offer = self.quantity * self.price
        super(Offer, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.item} + {self.item}+ {self.total_price_is_offer}+{self.quantity}' \
               f'+{self.type_function}+{self.price}'


class Balance(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    balance = models.DecimalField(max_digits=5, decimal_places=2, max_length=5, null=True, blank=True, default=400)

    def __str__(self):
        return f"{self.balance}"




    @receiver(post_save, sender=User)
    def create_user_balance(sender, instance, created, **kwargs):
        if created:
            Balance.objects.create(user=instance, balance=0)




class Trade(models.Model):
    client = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="client_trade",
                               related_query_name="client_trade")
    client_offer = models.ForeignKey('Offer', blank=True, null=True, on_delete=models.SET_NULL,
                                     related_name='client_offer_trade',
                                     related_query_name="client_offer_trade")
    quantity_client = models.DecimalField(max_digits=5, decimal_places=2, max_length=5, null=True, blank=True,
                                          default=400)
    price_total = models.DecimalField(max_digits=5, decimal_places=2, max_length=5, null=True, blank=True)

    seller = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="seller_trade",
                               related_query_name="seller_trade")
    seller_offer = models.ForeignKey('Offer', blank=True, null=True, on_delete=models.SET_NULL,
                                     related_name="seller_offer_trade",
                                     related_query_name="seller_offer_trade")
    quantity_seller = models.DecimalField(max_digits=5, decimal_places=2, max_length=5, null=True, blank=True,
                                          default=400)
    price_total_1 = models.DecimalField(max_digits=5, decimal_places=2, max_length=5, null=True, blank=True)

    def __str__(self):
        return f'{self.client} +{self.client_offer}+{self.quantity_client}+{self.price_total}+{self.seller}' \
               f'+{self.seller_offer}+{self.quantity_seller}+{self.price_total_1} '

    @receiver(post_save, sender=User)
    def create_user_balance(sender, instance, created, **kwargs):
        if created:
            p = Item.objects.first()
            Inventory.objects.create(user=instance, item_1=p, quantity=0)


class Inventory(models.Model):
    user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.CASCADE)
    item_1 = models.ForeignKey('Item', blank=True, null=True, on_delete=models.CASCADE, related_name="item_name_2",
                               related_query_name="item_name_2")
    quantity = models.DecimalField(max_digits=5, decimal_places=2, max_length=5, null=True, blank=True)

    def __str__(self):
        return f'{self.user} + {self.quantity} + {self.item_1}'

    #
    # @receiver(post_save, sender=Offer)
    # def create_user_balance(sender,  instance, created, **kwargs):
    #     if created:
    #         s = Inventory.objects.create(quantity=0)
    #         p = Offer.objects.filter(user=s.user)
    #         if p.quantity > s.quantity and p.type_function == 2:
    #             p.quantity = s.quantity - p.quantity
    #             instance.save()
    #         else:
    #             p.is_activate = False
    #             p.save()


