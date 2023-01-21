from .models import *
from django.contrib import admin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(CodeName)

admin.site.register(Currency)

admin.site.register(Item)

admin.site.register(WatchList)

admin.site.register(Offer)

admin.site.register(Trade)

admin.site.register(Inventory)

admin.site.register(Balance)
