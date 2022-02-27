from django.contrib import admin
from django.contrib.admin import TabularInline
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from core.models import User
from customers.models import Customer


class CustomerInline(TabularInline):
    model = Customer
    extra = 0


UserAdmin.list_display = ('id', 'phone', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser')
UserAdmin.list_display_links = ('phone',)
UserAdmin.ordering = ('-is_superuser', '-is_staff')
UserAdmin.search_fields = ('username', 'email', 'phone')
UserAdmin.inlines = [CustomerInline]
UserAdmin.add_fieldsets = (
    (None, {'classes': ('wide',), 'fields': ('phone', 'password1', 'password2'), }),
    (_('User_info'), {'classes': ('wide',), 'fields': ('first_name', 'last_name', 'email',)}),
    (_('User_permissions'), {'classes': ('wide',), 'fields': ('is_superuser', 'is_staff')})
)
UserAdmin.fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
admin.site.register(User, UserAdmin)
