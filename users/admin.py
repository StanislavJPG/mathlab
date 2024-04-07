import djoser.views
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    search_fields = ("username", "email")


admin.site.register(CustomUser, CustomUserAdmin)
