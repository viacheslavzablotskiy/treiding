from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView

from docker_admin.views import *
from django.contrib import admin
from django.urls import path, include, re_path

from docker_admin import views

router = routers.DefaultRouter()
router.register(r"api", ItemViewSet, basename="list_ap"),
router.register(r"valuta", Currency),
router.register(r"item", Item_table, basename="item"),
router.register(r'watch_list', WatchList_watchlist),
router.register(r"Offer", Offer_offer),
router.register(r"trade", Trade_trade),
router.register(r"inventory", Inventory_inventory),
router.register(r"balance/", Balance_balance),

urlpatterns = [
    path('admin/', admin.site.urls),
    path('verify/(?P<key>[a-z0-9\-]+)/', views.verify, name="verify"),
    path('api/log/', include("rest_framework.urls")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/auth/', include('djoser.urls')),

]
urlpatterns += router.urls
