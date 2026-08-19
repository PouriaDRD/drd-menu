from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest
from django.utils.html import format_html
from django.forms import ModelForm, ChoiceField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import UserModel
from accounts.enums import UserRole, UserStatus


@admin.register(UserModel)
class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for UserModel.
    """

    list_per_page = 50

    list_display = [
        "phone_number",
        "full_name",
        "status_badge",
        "last_login",
        "created_at",
    ]

    search_fields = [
        "phone_number",
        "first_name",
        "last_name",
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
        "is_superuser",
        "last_login",
        "updated_at",
        "created_at",
    ]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "id",
                    "phone_number",
                    "first_name",
                    "last_name",
                    "password",
                ),
            },
        ),
        (
            "Account",
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

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "role",
                    "status",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    @admin.display(description="Account", ordering="role")
    def status_badge(self, obj: UserModel):
        """
        Display role, account status and verification state.
        """

        role_icons: dict[str, str] = {
            str(UserRole.SUPERUSER): "🔵",
            str(UserRole.ADMIN): "🟢",
            str(UserRole.USER): "⚪",
        }

        status_colors: dict[str, str] = {
            "active": "#16a34a",
            "inactive": "#6b7280",
            "banned": "#dc2626",
        }

        role = UserRole(obj.role).label
        role_icon = role_icons.get(
            str(obj.role),
            "⚪",
        )

        status = UserStatus(obj.status).label
        status_color = status_colors.get(
            str(obj.status),
            "#6b7280",
        )

        return format_html(
            """
            {} {}
            ·
            <span style="color:{};font-weight:600;">
                {}
            </span>
            """,
            role_icon,
            role,
            status_color,
            status,
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

        role_field = form.base_fields.get("role")

        if isinstance(role_field, ChoiceField):

            if obj and obj.is_superuser:
                role_field.choices = [
                    (
                        UserRole.SUPERUSER,
                        UserRole.SUPERUSER.label,
                    ),
                ]

            else:
                role_field.choices = [
                    (
                        UserRole.USER,
                        UserRole.USER.label,
                    ),
                    (
                        UserRole.ADMIN,
                        UserRole.ADMIN.label,
                    ),
                ]

        return form
