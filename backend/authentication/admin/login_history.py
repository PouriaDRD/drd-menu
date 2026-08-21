from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from authentication.models import LoginHistoryModel

DEV = False


@admin.register(LoginHistoryModel)
class LoginHistoryAdmin(admin.ModelAdmin):
    """
    Login history admin panel.
    """

    list_display = (
        "user",
        "ip_address",
        "user_agent",
        "device",
        "browser",
        "operating_system",
        "country",
        "city",
        "is_successful",
        "updated_at",
        "created_at",
    )

    list_filter = (
        "is_successful",
        "created_at",
    )

    search_fields = (
        "user__email",
        "ip_address",
        "user_agent",
        "device",
        "browser",
        "operating_system",
        "country",
        "city",
    )

    readonly_fields = [
        "id",
        "user",
        "ip_address",
        "user_agent",
        "device",
        "browser",
        "operating_system",
        "country",
        "city",
        "is_successful",
        "failure_reason",
        "updated_at",
        "created_at",
    ]

    def has_add_permission(self, request):
        return DEV

    def has_delete_permission(self, request, obj=None):
        return DEV

    def has_change_permission(self, request, obj=None):
        return DEV

    def ip_address(self, obj):
        return mark_safe(format_html(f"<code>{obj.ip_address}</code>"))

    def user_agent(self, obj):
        return mark_safe(format_html(f"<code>{obj.user_agent}</code>"))

    def device(self, obj):
        return mark_safe(format_html(f"<code>{obj.device}</code>"))

    def browser(self, obj):
        return mark_safe(format_html(f"<code>{obj.browser}</code>"))

    def operating_system(self, obj):
        return mark_safe(format_html(f"<code>{obj.operating_system}</code>"))

    def country(self, obj):
        return mark_safe(format_html(f"<code>{obj.country}</code>"))

    def city(self, obj):
        return mark_safe(format_html(f"<code>{obj.city}</code>"))

    def failure_reason(self, obj):
        return mark_safe(format_html(f"<code>{obj.failure_reason}</code>"))
