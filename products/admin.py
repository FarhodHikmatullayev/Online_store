from django.contrib import admin

from .models import Product, Category, Cart, CartItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'price', 'created_time', 'category', 'updated_time')
    readonly_fields = ('created_time', 'updated_time')
    search_fields = ('user__username', 'name', 'price')
    list_filter = ('created_time', 'updated_time')
    date_hierarchy = 'created_time'


class CartItemInlineAdmin(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = (CartItemInlineAdmin,)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    pass
