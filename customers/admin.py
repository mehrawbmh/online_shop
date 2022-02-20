from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from customers.models import Customer, Address

admin.site.register(Address)
admin.site.register(Customer, UserAdmin)