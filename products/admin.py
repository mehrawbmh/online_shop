from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline

from .models import Discount, Product, Brand, Category


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['id', 'name', 'parent']
    list_display_links = ['name']
    ordering = ['parent']
    search_fields = ['name', 'parent']


@admin.register(Discount)
class DiscountAdmin(ModelAdmin):
    list_display = ['id', 'type', 'value', 'expire_date']
    ordering = ['type', 'expire_date']
    list_editable = ['expire_date']


@admin.action(description='Mark selected products as inactive')
def deactive(self, request, queryset):
    queryset.update(is_active=False)


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    fields = ['name', 'price', 'brand', 'category', 'discount', 'properties', 'image']
    list_display = ['name', 'price', 'brand', 'category', 'discount']
    list_display_links = ['name']
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
    ordering = ['name']
    search_fields = ['name']
