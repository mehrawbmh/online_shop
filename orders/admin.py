from django.contrib import admin
from django.contrib.admin import ModelAdmin

from orders.models import CartItem, Cart
from products.models import OffCode

admin.site.register(OffCode)


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    exclude = ['raw_price', 'order_discount']
    list_display = ['id', 'status', 'off_code', 'customer', 'address', 'product_list']


@admin.register(CartItem)
class CartItemAdmin(ModelAdmin):
    exclude = ['total_price']

