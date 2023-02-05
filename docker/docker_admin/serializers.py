from typing import Dict

from django.contrib.auth import authenticate
from rest_framework import serializers
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


class OfferSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Offer
        fields = '__all__'


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
