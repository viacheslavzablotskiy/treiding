from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView

from docker_admin.views import *
from django.contrib import admin
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r"api", ItemViewSet),
router.register(r"valuta", Curenccy),
router.register(r"item", Item_table),
router.register(r'watch_list', WathList_table),
router.register(r"Offer", Offer_offer),
router.register(r"trade", Trade_trade),
router.register(r"inventiry", Inventory_inventory),
router.register(r"balans/", Balans_balans),
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', include("rest_framework.urls")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/auth/', include('djoser.urls')),
]
urlpatterns += router.urls
