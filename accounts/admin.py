from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'shop_name', 'is_seller', 'phone')
    list_filter = ('is_seller',)
    search_fields = ('user__username', 'shop_name')