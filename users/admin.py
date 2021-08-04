from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import CustomUser


class CustomUserInline(admin.StackedInline):
    """Class to create possibility to add extended fields in the admin panel"""
    model = CustomUser
    can_delete = False
    verbose_name_plural = 'custom_user'


class CustomUserAdmin(UserAdmin):
    """Class to create possibility edit CustomUser model in User model in the admin panel"""
    inlines = (CustomUserInline,)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
