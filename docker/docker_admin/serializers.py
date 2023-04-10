from typing import Dict

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import OutstandingToken
from .models import *


class Register(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, write_only=True)
    access_token = serializers.CharField(max_length=100, read_only=True)
    refresh_token = serializers.CharField(max_length=100, read_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "access_token", "refresh_token")
        # extra_kwargs = {"password": {"write_only": True}, "access_token": {"read_only": True},
        #                 "refresh_token": {"read_only": True}}

    def create(self, validated_data: Dict):
        return User.objects.create_user(**validated_data)


class Register_token_in_the_account(serializers.ModelSerializer):
    class Meta:
        model = OutstandingToken
        fields = "__all__"


class CodeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeName
        fields = '__all__'


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class WatchListSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = WatchList
        fields = '__all__'




    # def create(self, validated_data):
    #     # title = InventorySerializers()
    #     try:
    #         offer = Offer(user=validated_data["user"],
    #                       item=validated_data["item"],
    #                       price=validated_data["price"]
    #                       total_price_is_offer=validated_data["total_price_is_offer"],
    #                       is_activate=validated_data["is_activate"],
    #                     )
    #         inventory = Inventory.objects.get(user=offer.user)
    #         if offer.quantity < inventory.quantity:
    #             offer.save(validated_data)
    #     except ValueError:
    #         print("you does not can to create because ")
    #     return offer

    # class UserSerializer(serializers.ModelSerializer):
    #     profile = ProfileSerializer()
    #
    #     class Meta:
    #         model = User
    #         fields = ('username', 'email', 'profile')
    #
    #     def create(self, validated_data):
    #         profile_data = validated_data.pop('profile')
    #         user = User.objects.create(**validated_data)
    #         Profile.objects.create(user=user, **profile_data)
    #         return user


class TradeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'


class InventorySerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Inventory
        fields = '__all__'


class BalanceSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Balance
        fields = "__all__"


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 10000


class OfferSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


    class Meta:
        model = Offer
        fields = "__all__"

    # def matrix(self):
    #     if Inventory.quantity > Offer.quantity:
    #         raise serializers.ValidationError('This field must be an even number.')
    #     return False
