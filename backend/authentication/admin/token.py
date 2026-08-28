from django.utils import timezone
from django.http import HttpRequest
from django.utils.html import format_html
from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

DEV = True


# =============================================================================
# Action: Delete Expired Tokens
# =============================================================================


@admin.action(
    description="Delete expired tokens from database",
)
def delete_expired_tokens(
    modeladmin,
    request: HttpRequest,
    queryset,
):
    """
    Delete tokens whose expires_at timestamp is earlier than current time.
    """

    now = timezone.now()
    expired_queryset = queryset.filter(expires_at__lt=now)
    count = expired_queryset.count()

    if count > 0:
        expired_queryset.delete()
        modeladmin.message_user(
            request,
            f"{count} expired token(s) deleted successfully.",
            level=messages.SUCCESS,
        )
    else:
        modeladmin.message_user(
            request,
            "No expired tokens were found in the selected items.",
            level=messages.WARNING,
        )


# =============================================================================
# Outstanding Tokens Admin
# =============================================================================

try:
    admin.site.unregister(OutstandingToken)
except admin.sites.NotRegistered:
    pass


@admin.register(OutstandingToken)
class OutstandingTokenAdmin(admin.ModelAdmin):
    """
    Admin configuration for SimpleJWT Outstanding Tokens.
    """

    list_per_page = 50
    ordering = ("-created_at", "-id")

    list_display = (
        "user_email_display",
        "jti_display",
        "expiration_badge",
        "expires_at_display",
        "created_at_display",
    )

    list_filter = (
        "expires_at",
        "created_at",
    )

    search_fields = (
        "user__email",
        "user__phone_number",
        "jti",
    )

    autocomplete_fields = ("user",)
    actions = (delete_expired_tokens,)

    readonly_fields = (
        "id",
        "jti",
        "token",
        "created_at",
        "expires_at",
    )

    fieldsets = (
        (
            "Token Details",
            {
                "fields": (
                    "id",
                    "user",
                    "jti",
                    "token",
                ),
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "expires_at",
                    "created_at",
                ),
            },
        ),
    )

    def get_queryset(self, request: HttpRequest):
        return (
            super().get_queryset(request).select_related("user").order_by("-created_at")
        )

    def has_add_permission(self, request: HttpRequest) -> bool:
        return DEV

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return DEV

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return DEV

    @admin.display(description="User", ordering="user__email")
    def user_email_display(self, obj: OutstandingToken):
        user = getattr(obj, "user", None)
        if not user:
            return format_html('<span style="opacity:.55;">{}</span>', "—")
        email_or_phone = getattr(user, "email", None) or getattr(
            user, "phone_number", str(user)
        )
        return format_html("<code>{}</code>", email_or_phone)

    @admin.display(description="JTI", ordering="jti")
    def jti_display(self, obj: OutstandingToken):
        jti = getattr(obj, "jti", None)
        if not jti:
            return format_html('<span style="opacity:.55;">{}</span>', "—")
        return format_html(
            '<code style="font-weight:600; padding:2px 6px; background:var(--accent-color-transparent, rgba(39, 103, 165, 0.1)); color:var(--message-info-fg, #2767a5); border-radius:4px;">{}</code>',
            str(jti)[:12] + "...",
        )

    @admin.display(description="Status", ordering="expires_at")
    def expiration_badge(self, obj: OutstandingToken):
        expires_at = getattr(obj, "expires_at", None)
        if expires_at and expires_at < timezone.now():
            return mark_safe("""
                <span style="
                    display:inline-flex;
                    align-items:center;
                    gap:6px;
                    color:var(--body-fg, #fff);
                    font-weight:500;
                ">
                    <span style="
                        width:7px;
                        height:7px;
                        border-radius:50%;
                        background:var(--message-error-fg, #ba2121);
                        flex:none;
                    "></span>
                    Expired
                </span>
            """)
        return mark_safe("""
            <span style="
                display:inline-flex;
                align-items:center;
                gap:6px;
                color:var(--body-fg, #fff);
                font-weight:500;
            ">
                <span style="
                    width:7px;
                    height:7px;
                    border-radius:50%;
                    background:var(--message-success-fg, #198754);
                    flex:none;
                "></span>
                Active
            </span>
        """)

    @admin.display(description="Expires At", ordering="expires_at")
    def expires_at_display(self, obj: OutstandingToken):
        return obj.expires_at

    @admin.display(description="Created", ordering="created_at")
    def created_at_display(self, obj: OutstandingToken):
        return obj.created_at


# =============================================================================
# Blacklisted Tokens Admin
# =============================================================================

try:
    admin.site.unregister(BlacklistedToken)
except admin.sites.NotRegistered:
    pass


@admin.register(BlacklistedToken)
class BlacklistedTokenAdmin(admin.ModelAdmin):
    """
    Admin configuration for SimpleJWT Blacklisted Tokens.
    """

    list_per_page = 50
    ordering = ("-blacklisted_at", "-id")

    list_display = (
        "token_user_display",
        "jti_display",
        "blacklisted_at_display",
    )

    list_filter = ("blacklisted_at",)

    search_fields = (
        "token__user__email",
        "token__user__phone_number",
        "token__jti",
    )

    autocomplete_fields = ("token",)

    readonly_fields = (
        "id",
        "blacklisted_at",
    )

    fieldsets = (
        (
            "Blacklist Details",
            {
                "fields": (
                    "id",
                    "token",
                ),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("blacklisted_at",),
            },
        ),
    )

    def get_queryset(self, request: HttpRequest):
        return (
            super()
            .get_queryset(request)
            .select_related("token", "token__user")
            .order_by("-blacklisted_at")
        )

    def has_add_permission(self, request: HttpRequest) -> bool:
        return DEV

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return DEV

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return DEV

    @admin.display(description="User", ordering="token__user__email")
    def token_user_display(self, obj: BlacklistedToken):
        token = getattr(obj, "token", None)
        if not token or not getattr(token, "user", None):
            return format_html('<span style="opacity:.55;">{}</span>', "—")
        user = token.user
        email_or_phone = getattr(user, "email", None) or getattr(
            user, "phone_number", str(user)
        )
        return format_html("<code>{}</code>", email_or_phone)

    @admin.display(description="JTI", ordering="token__jti")
    def jti_display(self, obj: BlacklistedToken):
        token = getattr(obj, "token", None)
        if not token or not getattr(token, "jti", None):
            return format_html('<span style="opacity:.55;">{}</span>', "—")
        return format_html(
            '<code style="font-weight:600; padding:2px 6px; background:rgba(186, 33, 33, 0.1); color:var(--message-error-fg, #ba2121); border-radius:4px;">{}</code>',
            str(token.jti)[:12] + "...",
        )

    @admin.display(description="Blacklisted At", ordering="blacklisted_at")
    def blacklisted_at_display(self, obj: BlacklistedToken):
        return obj.blacklisted_at
