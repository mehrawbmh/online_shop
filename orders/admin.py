from django.contrib import admin

from orders.models import CartItem, Cart
from products.models import OffCode

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OffCode)
