from django.contrib import admin
from common.models import (
    User
)

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _


@admin.register(User)
class UserAdmin(BaseUserAdmin, admin.ModelAdmin):
    ordering = ('email',)
    exclude = [
        'password', 'groups', 'user_permissions', 'username', 'date_joined',
        'role'
    ]
    readonly_fields = ['last_login', 'created_on']
    list_display = ['__str__', ]

    fieldsets = (
        (_("Personal info"), {
            "fields": (
                "email",
                "first_name",
                "last_name",
                "phone_number",
            )
            }),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "type"
                ),
            },
        ),
        (_("Important dates"), {
            "fields": (
                "last_login",
                "created_on",
            )
        }),
        (None, {"fields": ("password",)}),
    )

    add_fieldsets = (
        (_("Personal info"), {
            "fields": (
                "email",
                "first_name",
                "last_name",
            )
            }),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (_("Important dates"), {
            "fields": (
                "last_login",
                "created_on",
            )
        }),
        (None, {"fields": ("password1", "password2")}),
    )