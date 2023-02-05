from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView

from docker_admin.views import *
from django.contrib import admin
from django.urls import path, include

from docker_admin import views

router = routers.DefaultRouter()
router.register(r"api", ItemViewSet, basename="list_ap"),
router.register(r"valuta", Currency),
router.register(r"item", Item_table, basename="item"),
router.register(r'watch_list', WatchList_watchlist),
router.register(r"Offer", Offer_offer),
router.register(r"token", Register_token_in_the_views, basename="token"),
router.register(r"trade", Trade_trade),
router.register(r"inventory", Inventory_inventory),
router.register(r"balance/", Balance_balance),

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/log/', include("rest_framework.urls")),
    path("register/", views.Register_user.as_view(), name="create-user"),
    # path("token/", views.Register_token_in_the_views.as_view({'get': 'get_rank'}), name="token"),
    # path("login/", views.User_sees_him_token.as_view(), name="login-user"),
    # path('verify/(?P<key>[a-z0-9\-]+)/', views.verify, name="verify"),
    # path("token/", views.Register_in_the_blacklist.as_view(), name="token-list"),
    # path('api/login/', include("rest_framework.urls")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/auth/', include('djoser.urls')),

]
urlpatterns += router.urls
