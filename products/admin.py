from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline

from .models import Discount, Product, Brand, Category

admin.site.register(Category)
admin.site.register(Discount)


@admin.action(description='Mark selected products as inactive')
def deactive(self, request, queryset):
    queryset.update(is_active=False)


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    fields = ['name', 'price', 'brand', 'category', 'discount']
    list_display = ['name', 'price', 'brand', 'category', 'discount']
    list_display_links = ['name']
    list_editable = ['discount']
    search_fields = ['name', 'brand__name', 'category__name']
    actions = [deactive]
    autocomplete_fields = ['brand']


class ProductInline(StackedInline):
    model = Product
    extra = 1


@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ['id', 'name', 'satisfaction_rate']
    list_display_links = ['id', 'name']
    inlines = [ProductInline]
    search_fields = ['name']
