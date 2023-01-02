from rest_framework import serializers
from .models import *


class CodeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeName
        fields = '__all__'


class CurenccySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'


class PriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = '__all__'


class WatchListSerialisers(serializers.ModelSerializer):

    class Meta:
        model = WatchList
        fields = '__all__'


class OfferSerialisers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Offer
        fields = '__all__'



class TradeSerialisers(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'


class InventorySerialisers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Inventory
        fields = '__all__'


class BalansSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Balans
        fields = "__all__"









