from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.forms import ChoiceField, ModelForm
from django.http import HttpRequest
from django.utils.html import format_html

from accounts.enums import UserRole, UserStatus
from accounts.models import UserModel


@admin.register(UserModel)
class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for UserModel.

    The interface follows Django Admin's native visual language
    and supports both light and dark themes.
    """

    # =========================================================================
    # General
    # =========================================================================

    list_per_page = 50

    ordering = ("-created_at",)

    # =========================================================================
    # List (user_display contains both name and phone)
    # =========================================================================

    list_display = (
        "user_display",
        "role_badge",
        "status_badge",
        "last_login_display",
        "created_at_display",
    )

    list_filter = (
        "role",
        "status",
        "created_at",
    )

    search_fields = (
        "phone_number",
        "first_name",
        "last_name",
    )

    # =========================================================================
    # Actions
    # =========================================================================

    actions = (
        "activate_users",
        "deactivate_users",
        "ban_users",
        "unban_users",
    )

    # -------------------------------------------------------------------------
    # Activate
    # -------------------------------------------------------------------------

    @admin.action(
        description="Activate selected users",
    )
    def activate_users(
        self,
        request: HttpRequest,
        queryset,
    ):
        """
        Activate selected users.

        Superusers are excluded from bulk status changes.
        """

        updated_count = (
            queryset.filter(
                is_superuser=False,
            )
            .exclude(
                status=UserStatus.ACTIVE,
            )
            .update(
                status=UserStatus.ACTIVE,
            )
        )

        self.message_user(
            request,
            f"{updated_count} user(s) activated successfully.",
        )

    # -------------------------------------------------------------------------
    # Deactivate
    # -------------------------------------------------------------------------

    @admin.action(
        description="Deactivate selected users",
    )
    def deactivate_users(
        self,
        request: HttpRequest,
        queryset,
    ):
        """
        Deactivate selected users.

        Superusers are excluded from bulk status changes.
        """

        updated_count = (
            queryset.filter(
                is_superuser=False,
            )
            .exclude(
                status=UserStatus.INACTIVE,
            )
            .update(
                status=UserStatus.INACTIVE,
            )
        )

        self.message_user(
            request,
            f"{updated_count} user(s) deactivated successfully.",
        )

    # -------------------------------------------------------------------------
    # Ban
    # -------------------------------------------------------------------------

    @admin.action(
        description="Ban selected users",
    )
    def ban_users(
        self,
        request: HttpRequest,
        queryset,
    ):
        """
        Ban selected users.

        Superusers are excluded from bulk status changes.
        """

        updated_count = (
            queryset.filter(
                is_superuser=False,
            )
            .exclude(
                status=UserStatus.BANNED,
            )
            .update(
                status=UserStatus.BANNED,
            )
        )

        self.message_user(
            request,
            f"{updated_count} user(s) banned successfully.",
        )

    # -------------------------------------------------------------------------
    # Unban
    # -------------------------------------------------------------------------

    @admin.action(
        description="Unban selected users",
    )
    def unban_users(
        self,
        request: HttpRequest,
        queryset,
    ):
        """
        Unban selected users.

        Unbanned users become active.
        Superusers are excluded from bulk status changes.
        """

        updated_count = queryset.filter(
            is_superuser=False,
            status=UserStatus.BANNED,
        ).update(
            status=UserStatus.ACTIVE,
        )

        self.message_user(
            request,
            f"{updated_count} user(s) unbanned successfully.",
        )

    # =========================================================================
    # Detail
    # =========================================================================

    readonly_fields = (
        "id",
        "is_superuser",
        "last_login",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "User",
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
            "Dates",
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

    # =========================================================================
    # Add User
    # =========================================================================

    add_fieldsets = (
        (
            "Create User",
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "first_name",
                    "last_name",
                    "role",
                    "status",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    # =========================================================================
    # User Display (Combines Name & Phone stacked)
    # =========================================================================

    @admin.display(
        description="User / Phone",
        ordering="first_name",
    )
    def user_display(
        self,
        obj: UserModel,
    ):
        """
        Display user's full name and phone number stacked vertically.
        """

        full_name = obj.full_name.strip()
        phone_number = getattr(obj, "phone_number", None)

        if full_name and phone_number:
            return format_html(
                "<strong>{}</strong><br>"
                '<code style="color:var(--body-quiet-color, #666); font-size:12px;">{}</code>',
                full_name,
                phone_number,
            )

        if full_name:
            return format_html(
                "<strong>{}</strong>",
                full_name,
            )

        if phone_number:
            return format_html(
                "<code>{}</code>",
                phone_number,
            )

        return format_html(
            '<span style="opacity:.65;">{}</span>',
            "Unnamed user",
        )

    # =========================================================================
    # Role
    # =========================================================================

    @admin.display(
        description="Role",
        ordering="role",
    )
    def role_badge(
        self,
        obj: UserModel,
    ):
        """
        Display user's role using a subtle semantic indicator.
        """

        role = str(obj.role)

        role_config = {
            str(UserRole.SUPERUSER): {
                "label": UserRole.SUPERUSER.label,
                "color": "var(--message-warning-fg, #996a00)",
                "icon": "★",
            },
            str(UserRole.ADMIN): {
                "label": UserRole.ADMIN.label,
                "color": "var(--message-info-fg, #2767a5)",
                "icon": "●",
            },
            str(UserRole.USER): {
                "label": UserRole.USER.label,
                "color": "var(--body-quiet-color, #666)",
                "icon": "●",
            },
        }

        config = role_config.get(
            role,
            {
                "label": "Unknown",
                "color": "var(--body-quiet-color, #666)",
                "icon": "●",
            },
        )

        return format_html(
            """
            <span style="
                display:inline-flex;
                align-items:center;
                gap:6px;
                white-space:nowrap;
            ">
                <span style="
                    color:{};
                    font-size:10px;
                    line-height:1;
                ">
                    {}
                </span>

                <span style="
                    color:var(--body-fg, #333);
                    font-weight:500;
                ">
                    {}
                </span>
            </span>
            """,
            config["color"],
            config["icon"],
            config["label"],
        )

    # =========================================================================
    # Status
    # =========================================================================

    @admin.display(
        description="Status",
        ordering="status",
    )
    def status_badge(
        self,
        obj: UserModel,
    ):
        """
        Display account status using a subtle status indicator.
        """

        status = str(obj.status)

        status_config = {
            str(UserStatus.ACTIVE): {
                "label": UserStatus.ACTIVE.label,
                "color": "var(--message-success-fg, #198754)",
            },
            str(UserStatus.INACTIVE): {
                "label": UserStatus.INACTIVE.label,
                "color": "var(--body-quiet-color, #777)",
            },
            str(UserStatus.BANNED): {
                "label": UserStatus.BANNED.label,
                "color": "var(--message-error-fg, #ba2121)",
            },
        }

        config = status_config.get(
            status,
            {
                "label": "Unknown",
                "color": "var(--body-quiet-color, #777)",
            },
        )

        return format_html(
            """
            <span style="
                display:inline-flex;
                align-items:center;
                gap:7px;
                white-space:nowrap;
            ">
                <span style="
                    width:7px;
                    height:7px;
                    border-radius:50%;
                    background:{};
                    flex:none;
                "></span>

                <span style="
                    color:var(--body-fg, #333);
                    font-weight:500;
                ">
                    {}
                </span>
            </span>
            """,
            config["color"],
            config["label"],
        )

    # =========================================================================
    # Last Login
    # =========================================================================

    @admin.display(
        description="Last login",
        ordering="last_login",
    )
    def last_login_display(
        self,
        obj: UserModel,
    ):
        """
        Display the last login timestamp.
        """

        if not obj.last_login:
            return format_html(
                '<span style="opacity:.55;">{}</span>',
                "Never",
            )

        return obj.last_login

    # =========================================================================
    # Created At
    # =========================================================================

    @admin.display(
        description="Created",
        ordering="created_at",
    )
    def created_at_display(
        self,
        obj: UserModel,
    ):
        """
        Display user creation timestamp.
        """

        return obj.created_at

    # =========================================================================
    # Permissions
    # =========================================================================

    def get_form(
        self,
        request: HttpRequest,
        obj: UserModel | None = None,
        change: bool = False,
        **kwargs,
    ) -> type[ModelForm]:
        """
        Restrict available role choices.

        Existing superusers can only remain superusers.
        Normal users can only be USER or ADMIN.
        """

        form = super().get_form(
            request=request,
            obj=obj,
            change=change,
            **kwargs,
        )

        role_field = form.base_fields.get(
            "role",
        )

        if not isinstance(
            role_field,
            ChoiceField,
        ):
            return form

        if obj and obj.is_superuser:
            role_field.choices = (
                (
                    UserRole.SUPERUSER,
                    UserRole.SUPERUSER.label,
                ),
            )

        else:
            role_field.choices = (
                (
                    UserRole.USER,
                    UserRole.USER.label,
                ),
                (
                    UserRole.ADMIN,
                    UserRole.ADMIN.label,
                ),
            )

        return form
