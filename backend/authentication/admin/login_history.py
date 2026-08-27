from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from authentication.models import LoginHistoryModel

DEV = True


@admin.register(LoginHistoryModel)
class LoginHistoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for login history records.

    Login history is an audit-oriented model and should normally be
    read-only in production.
    """

    # ======================================================================
    # List
    # ======================================================================

    list_display = (
        "user_display",
        "status_badge",
        "ip_address_display",
        "device_display",
        "browser_display",
        "operating_system_display",
        "location_display",
        "created_at",
    )

    list_filter = (
        "is_successful",
        "device",
        # "operating_system",
        # "browser",
        # "country",
        # "country_code",
        # "region",
        # "city",
        "created_at",
    )

    search_fields = (
        "user__phone_number",
        "ip_address",
    )

    autocomplete_fields = ("user",)

    ordering = (
        "-created_at",
        "-id",
    )

    list_per_page = 50

    list_select_related = ("user",)

    # ======================================================================
    # Detail
    # ======================================================================

    readonly_fields = (
        "id",
        "user",
        "ip_address",
        "user_agent_display",
        "device_display",
        "browser_display",
        "operating_system_display",
        "country",
        "country_code",
        "region",
        "city",
        "coordinates_display",
        "is_successful",
        "failure_reason_display",
        "updated_at",
        "created_at",
    )

    fieldsets = (
        (
            "Authentication",
            {
                "fields": (
                    "id",
                    "user",
                    "is_successful",
                    "failure_reason_display",
                ),
            },
        ),
        (
            "Network",
            {
                "fields": ("ip_address",),
            },
        ),
        (
            "Device",
            {
                "fields": ("device_display",),
            },
        ),
        (
            "Browser",
            {
                "fields": ("browser_display",),
            },
        ),
        (
            "Operating System",
            {
                "fields": ("operating_system_display",),
            },
        ),
        (
            "Location",
            {
                "fields": (
                    "country",
                    "country_code",
                    "region",
                    "city",
                    "coordinates_display",
                ),
            },
        ),
        (
            "User Agent",
            {
                "fields": ("user_agent_display",),
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    # ======================================================================
    # Permissions
    # ======================================================================

    def has_add_permission(self, request):
        return DEV

    def has_change_permission(self, request, obj=None):
        return DEV

    def has_delete_permission(self, request, obj=None):
        return DEV

    # ======================================================================
    # User
    # ======================================================================

    @admin.display(description="User")
    def user_display(self, obj):
        user = obj.user

        phone_number = getattr(
            user,
            "phone_number",
            None,
        )

        if phone_number:
            return format_html(
                "<code>{}</code>",
                phone_number,
            )

        return str(user)

    # ======================================================================
    # Status
    # ======================================================================

    @admin.display(description="Status", ordering="is_successful")
    def status_badge(self, obj):
        if obj.is_successful:
            return mark_safe(
                '<span style="'
                "display:inline-flex;"
                "align-items:center;"
                "padding:4px 9px;"
                "border-radius:999px;"
                "font-size:12px;"
                "font-weight:600;"
                "background:#dcfce7;"
                "color:#166534;"
                '">'
                "✓ Successful"
                "</span>"
            )

        return mark_safe(
            '<span style="'
            "display:inline-flex;"
            "align-items:center;"
            "padding:4px 9px;"
            "border-radius:999px;"
            "font-size:12px;"
            "font-weight:600;"
            "background:#fee2e2;"
            "color:#991b1b;"
            '">'
            "✕ Failed"
            "</span>"
        )

    # ======================================================================
    # IP
    # ======================================================================

    @admin.display(description="IP Address", ordering="ip_address")
    def ip_address_display(self, obj):
        if not obj.ip_address:
            return "—"

        return format_html(
            "<code>{}</code>",
            obj.ip_address,
        )

    # ======================================================================
    # Device
    # ======================================================================

    @admin.display(description="Device", ordering="device")
    def device_display(self, obj):
        device = obj.device or "Unknown"
        family = obj.device_family

        if family:
            return format_html(
                "<strong>{}</strong><br>"
                '<span style="color:#6b7280;font-size:12px;">'
                "{}"
                "</span>",
                device,
                family,
            )

        return device

    # ======================================================================
    # Browser
    # ======================================================================

    @admin.display(description="Browser", ordering="browser")
    def browser_display(self, obj):
        if not obj.browser:
            return "—"

        if obj.browser_version:
            return format_html(
                "<strong>{}</strong> " '<span style="color:#6b7280;">{}</span>',
                obj.browser,
                obj.browser_version,
            )

        return obj.browser

    # ======================================================================
    # Operating System
    # ======================================================================

    @admin.display(description="Operating System", ordering="operating_system")
    def operating_system_display(self, obj):
        if not obj.operating_system:
            return "—"

        if obj.operating_system_version:
            return format_html(
                "<strong>{}</strong> " '<span style="color:#6b7280;">{}</span>',
                obj.operating_system,
                obj.operating_system_version,
            )

        return obj.operating_system

    # ======================================================================
    # Location
    # ======================================================================

    @admin.display(description="Location")
    def location_display(self, obj):
        city = obj.city
        region = obj.region
        country = obj.country
        country_code = obj.country_code

        if not any(
            (
                city,
                region,
                country,
                country_code,
            )
        ):
            return "—"

        main_location = city or region or country or country_code

        secondary = []

        if region and region != main_location:
            secondary.append(region)

        if country and country != main_location:
            secondary.append(country)

        if country_code:
            secondary.append(country_code.upper())

        if secondary:
            return format_html(
                "<strong>{}</strong><br>"
                '<span style="color:#6b7280;font-size:12px;">'
                "{}"
                "</span>",
                main_location,
                " • ".join(secondary),
            )

        return format_html(
            "<strong>{}</strong>",
            main_location,
        )

    # ======================================================================
    # Coordinates
    # ======================================================================

    @admin.display(description="Coordinates")
    def coordinates_display(self, obj):
        latitude = getattr(
            obj,
            "latitude",
            None,
        )

        longitude = getattr(
            obj,
            "longitude",
            None,
        )

        if latitude is None or longitude is None:
            return "—"

        return format_html(
            "<code>{}, {}</code>",
            latitude,
            longitude,
        )

    # ======================================================================
    # User Agent
    # ======================================================================

    @admin.display(description="User Agent")
    def user_agent_display(self, obj):
        if not obj.user_agent:
            return "—"

        return format_html(
            '<div style="'
            "max-width:900px;"
            "overflow-wrap:anywhere;"
            "white-space:normal;"
            '">'
            "<code>{}</code>"
            "</div>",
            obj.user_agent,
        )

    # ======================================================================
    # Failure Reason
    # ======================================================================

    @admin.display(description="Failure Reason")
    def failure_reason_display(self, obj):
        if not obj.failure_reason:
            return "—"

        return format_html(
            '<div style="'
            "max-width:900px;"
            "overflow-wrap:anywhere;"
            "white-space:normal;"
            '">'
            "<code>{}</code>"
            "</div>",
            obj.failure_reason,
        )
