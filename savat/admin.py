from django.contrib import admin

from savat.models import Savat


@admin.register(Savat)
class SavatAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'price', 'created_time')
    search_fields = ('user__username', 'product__name')
    date_hierarchy = 'created_time'
    readonly_fields = ('created_time',)
