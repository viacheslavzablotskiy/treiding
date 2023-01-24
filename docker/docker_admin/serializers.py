from rest_framework import serializers
from .models import *


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


