from django.contrib import admin
from .models import Discount, Product, Brand, Category
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Discount)

