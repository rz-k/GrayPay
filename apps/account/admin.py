from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.account.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    list_display = ("id", "email", "username", "first_name", "last_name", "is_active")
    list_filter = ("is_active",)

    fieldsets = (
        (None, {
            'fields': ('email',"username", 'password')
        }),
        ('Personal info', {
            'fields': (
                'first_name',
                'last_name', 'phone_number')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff',
                'is_superuser',
                'groups', 'user_permissions')
        })
    )

    search_fields = ('email', 'first_name',"username")
    ordering = ('-id', 'email')
    list_editable = ("username", "email")
