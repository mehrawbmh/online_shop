from django.contrib import admin
from django.contrib.admin import TabularInline
from django.contrib.auth.admin import UserAdmin

from core.models import User
from customers.models import Customer


class CustomerInline(TabularInline):
    model = Customer
    extra = 0


UserAdmin.list_display = ('username', 'email', 'phone', 'is_staff')
UserAdmin.search_fields = ('username', 'email', 'phone')
UserAdmin.inlines = [CustomerInline]
admin.site.register(User, UserAdmin)
