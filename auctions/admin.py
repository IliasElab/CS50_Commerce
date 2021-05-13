from django.contrib import admin
from .models import *

# Register your models here.

class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "price", "category", "createdby", "isactive")

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'password', 'is_staff', 'is_active')
    filter_horizontal = ("watchlist",)

admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(User, UserAdmin)

