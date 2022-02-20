from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import User

UserAdmin.list_display = ('username', 'email', 'phone', 'is_staff')
UserAdmin.search_fields = ('username', 'email', 'phone')
admin.site.register(User, UserAdmin)
