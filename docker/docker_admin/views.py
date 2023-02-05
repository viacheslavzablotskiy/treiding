from django.http import Http404
from rest_framework import mixins, viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from .permissoins import IsOwnerOrReadOnly, IsAdminOrReadOnly, AdminOrReadOnly
from .serializers import *
from docker_admin.models import *
from django.shortcuts import HttpResponse, redirect


class Register_user(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = Register

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Register_token_in_the_views(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = OutstandingToken.objects.all()
    serializer_class = Register_token_in_the_account
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticated, IsOwnerOrReadOnly, AdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        user.is_verified = True
        user.save()
        return OutstandingToken.objects.filter(user=user)


class ItemViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = CodeName.objects.all()
    serializer_class = CodeNameSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, IsAuthenticated,
                          IsAdminOrReadOnly,)


class Currency(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated,
                          IsAdminOrReadOnly,)


class Item_table(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, IsAuthenticated,
                          IsAdminOrReadOnly,)


class WatchList_watchlist(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                          mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializers
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, IsAdminOrReadOnly, IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return WatchList.objects.filter(user=user.id)


class Offer_offer(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                  mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializers
    permission_classes = (IsAuthenticatedOrReadOnly, AdminOrReadOnly, IsOwnerOrReadOnly)



class Trade_trade(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializers
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, IsAdminOrReadOnly, IsAuthenticated)


class Inventory_inventory(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializers
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, IsAdminOrReadOnly, IsAuthenticated)

    def get_queryset(self):
        user = self.request.user
        return Inventory.objects.filter(user=user.id)


class Balance_balance(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializers
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, IsAdminOrReadOnly, IsAuthenticated)

    def get_queryset(self):
        user = self.request.user
        return Balance.objects.filter(user=user.id)
