from rest_framework import routers

from docker_admin.views import *
from django.contrib import admin
from django.urls import path

router = routers.DefaultRouter()
router.register(r"api", ItemViewSet),
router.register(r"valuta", Curenccy),
router.register(r"item", Item_table),
router.register(r"price", Price_price),
router.register(r'watch_list', WathList_table),
router.register(r"Offer", Offer_offer),
router.register(r"trade", Trade_trade),
router.register(r"inventiry", Inventory_inventory),
router.register(r"balans/", Balans_balans),
urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns += router.urls
