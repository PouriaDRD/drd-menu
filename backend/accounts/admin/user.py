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
        "role_badge",
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

    @admin.display(description="Role", ordering="role")
    def role_badge(self, obj: UserModel):
        """
        Display user role badge.
        """

        roles = {
            str(UserRole.SUPERUSER): ("👑", "#7c3aed"),
            str(UserRole.ADMIN): ("🛡️", "#2563eb"),
            str(UserRole.USER): ("👤", "#6b7280"),
        }

        icon, color = roles.get(
            str(obj.role),
            ("❓", "#6b7280"),
        )

        try:
            label = UserRole(obj.role).label
        except ValueError:
            label = "Unknown"

        return format_html(
            """
            <span style="
                color:{};
                font-weight:600;
            ">
                {} {}
            </span>
            """,
            color,
            icon,
            label,
        )

    @admin.display(description="Status", ordering="status")
    def status_badge(self, obj: UserModel):
        """
        Display account status badge.
        """

        statuses = {
            str(UserStatus.ACTIVE): ("●", "#16a34a"),
            str(UserStatus.INACTIVE): ("●", "#6b7280"),
            str(UserStatus.BANNED): ("●", "#dc2626"),
        }

        icon, color = statuses.get(
            str(obj.status),
            ("●", "#6b7280"),
        )

        try:
            label = UserStatus(obj.status).label
        except ValueError:
            label = "Unknown"

        return format_html(
            """
            <span style="
                color:{};
                font-weight:600;
            ">
                {} {}
            </span>
            """,
            color,
            icon,
            label,
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
