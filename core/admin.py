from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['username', 'email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {
            'fields': ('username',)
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_superuser', 'is_staff')
        }),
        (_('Important dates'), {
            'fields': ('last_login',)
        })
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')
        }),
    )

admin.site.register(models.User, UserAdmin)