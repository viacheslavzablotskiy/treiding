from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from .permissoins import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .serializers import *
from docker_admin.models import *

from django.shortcuts import HttpResponse


class ItemViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = CodeName.objects.all()
    serializer_class = CodeNameSerializer



class Currency(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer



class Item_table(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer



class WatchList_watchlist(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                          mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializers





class Offer_offer(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializers



class Trade_trade(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializers



class Inventory_inventory(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializers





class Balance_balance(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializers


