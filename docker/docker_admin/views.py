
from django.http import Http404
from rest_framework import mixins, viewsets, permissions
from rest_framework.permissions import IsAuthenticated

from .permissoins import IsOwnerOrReadOnly, IsAdminOrReadOnly, AdminOrReadOnly
from .serializers import *
from docker_admin.models import *
import uuid
from django.shortcuts import HttpResponse, redirect


def verify(request, key):
    try:
        token = Token.objects.get(key=key)
        user = User.objects.get(id=token.user_id)
    except User.DoesNotExist or Token.DoesNotExist:
        raise Http404("User does not exist or is already verified")
    # user.is_verified = False
    # user.save()
    token.user.is_verified = True
    token.user.save()
    return HttpResponse(f"добро пожаловать, твой токен {token.key}")


class ItemViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = CodeName.objects.all()
    serializer_class = CodeNameSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated,
                          IsAdminOrReadOnly,)


class Currency(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated,
                          IsAdminOrReadOnly,)


class Item_table(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated,
                          IsAdminOrReadOnly,)


class WatchList_watchlist(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                          mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializers
    permission_classes = (IsOwnerOrReadOnly, IsAdminOrReadOnly, IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return WatchList.objects.filter(user=user.id)


class Offer_offer(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                  mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializers
    permission_classes = (AdminOrReadOnly, IsOwnerOrReadOnly)


class Trade_trade(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializers
    permission_classes = (IsOwnerOrReadOnly, IsAdminOrReadOnly, IsAuthenticated)


class Inventory_inventory(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializers
    permission_classes = (IsOwnerOrReadOnly, IsAdminOrReadOnly, IsAuthenticated)

    def get_queryset(self):
        user = self.request.user
        return Inventory.objects.filter(user=user.id)


class Balance_balance(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializers
    permission_classes = (IsOwnerOrReadOnly, IsAdminOrReadOnly, IsAuthenticated)

    def get_queryset(self):
        user = self.request.user
        return Balance.objects.filter(user=user.id)
