from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import UserModel
from accounts.enums import UserRole


@admin.register(UserModel)
class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for UserModel.
    """

    list_per_page = 50

    list_display = [
        # basic information
        "username",
        "full_name",
        "email",
        "phone_number",
        # permissions
        "role",
        "status",
        # dates
        "last_login",
        "updated_at",
        "created_at",
    ]

    search_fields = [
        "username",
        "email",
        "phone_number",
    ]

    list_filter = [
        "role",
        "status",
    ]

    ordering = [
        "-created_at",
    ]

    readonly_fields = [
        "id",
        # "role",
        "is_superuser",
        "last_login",
        "updated_at",
        "created_at",
    ]

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "role",
                    "status",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "id",
                    "username",
                    "email",
                    "phone_number",
                    "first_name",
                    "last_name",
                    "password",
                ),
            },
        ),
        (
            "Role & Status",
            {
                "fields": (
                    "role",
                    "status",
                    "is_superuser",
                ),
            },
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "last_login",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
        (
            "Permissions",
            {
                "classes": ("collapse",),
                "fields": (
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    def get_form(
        self,
        request: HttpRequest,
        obj: UserModel | None = None,
        change: bool = False,
        **kwargs,
    ) -> type[ModelForm]:
        form = super().get_form(
            request=request,
            obj=obj,
            change=change,
            **kwargs,
        )

        # If the user is a superuser, allow all roles to be selected.
        if obj and obj.is_superuser:
            form.base_fields["role"].choices = [  # type: ignore
                (UserRole.SUPERUSER, UserRole.SUPERUSER.label),
            ]
            return form

        if "role" in form.base_fields:
            form.base_fields["role"].choices = [  # type: ignore
                (UserRole.USER, UserRole.USER.label),
                (UserRole.ADMIN, UserRole.ADMIN.label),
            ]

        return form
