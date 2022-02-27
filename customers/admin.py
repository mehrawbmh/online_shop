from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline

from customers.models import Customer, Address


# class UserInline(TabularInline):
#     model = User
class AddressInline(TabularInline):
    model = Address
    extra = 1


@admin.register(Customer)
class CustomerAdmin(ModelAdmin):
    list_display = ['id', 'user', 'birthday', 'national_code']
    list_display_links = ['id']
    inlines = [AddressInline]
    empty_value_display = 'EMPTY'


admin.site.register(Address)
