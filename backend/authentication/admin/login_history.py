from django.utils import timezone
from django.http import HttpRequest
from django.utils.html import format_html
from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from authentication.models import LoginHistoryModel

DEV = True


@admin.register(LoginHistoryModel)
class LoginHistoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for login history records.
    """

    list_per_page = 50

    ordering = (
        "-created_at",
        "-id",
    )

    show_facets = admin.ShowFacets.NEVER  # type: ignore

    list_display = (
        "user_display",
        "status_badge",
        "ip_address_display",
        "device_display",
        "browser_display",
        "operating_system_display",
        "location_display",
        "created_at_display",
    )

    list_filter = (
        "is_successful",
        "created_at",
    )

    search_fields = (
        "user__phone_number",
        "user__first_name",
        "user__last_name",
        "ip_address",
        "browser",
        "operating_system",
        "country",
        "city",
    )

    readonly_fields = (
        "id",
        "user",
        "ip_address",
        "device_display",
        "browser_display",
        "operating_system_display",
        "country",
        "country_code",
        "region",
        "city",
        "coordinates_display",
        "user_agent_display",
        "is_successful",
        "failure_reason_display",
        "created_at",
        "updated_at",
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

    def get_queryset(self, request: HttpRequest):
        return (
            super().get_queryset(request).select_related("user").order_by("-created_at")
        )

    def has_add_permission(self, request: HttpRequest) -> bool:
        return DEV

    def has_change_permission(
        self, request: HttpRequest, obj: LoginHistoryModel | None = None
    ) -> bool:
        return DEV

    def has_delete_permission(
        self, request: HttpRequest, obj: LoginHistoryModel | None = None
    ) -> bool:
        return DEV

    @admin.display(
        description="User",
        ordering="user__first_name",
    )
    def user_display(self, obj: LoginHistoryModel):
        user = getattr(obj, "user", None)
        if not user:
            return format_html('<span style="opacity:.55;">{}</span>', "—")

        full_name = getattr(user, "full_name", "").strip()
        phone_number = getattr(user, "phone_number", None)

        if full_name and phone_number:
            return format_html(
                "<strong>{}</strong><br>"
                '<span style="color:var(--body-quiet-color); font-size:12px;">{}</span>',
                full_name,
                phone_number,
            )

        if full_name:
            return format_html("<strong>{}</strong>", full_name)

        if phone_number:
            return format_html("<code>{}</code>", phone_number)

        return str(user)

    @admin.display(
        description="Status",
        ordering="is_successful",
    )
    def status_badge(self, obj: LoginHistoryModel):
        if getattr(obj, "is_successful", False):
            return mark_safe("""
                <span style="
                    display:inline-flex;
                    align-items:center;
                    gap:6px;
                    white-space:nowrap;
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
                    Successful
                </span>
                """)

        return mark_safe("""
            <span style="
                display:inline-flex;
                align-items:center;
                gap:6px;
                white-space:nowrap;
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
                Failed
            </span>
            """)

    @admin.display(description="IP Address", ordering="ip_address")
    def ip_address_display(self, obj: LoginHistoryModel):
        ip = getattr(obj, "ip_address", None)
        if not ip:
            return format_html('<span style="opacity:.55;">{}</span>', "—")
        return format_html("<code>{}</code>", ip)

    @admin.display(description="Device", ordering="device")
    def device_display(self, obj: LoginHistoryModel):
        device = getattr(obj, "device", None) or "Unknown"
        family = getattr(obj, "device_family", None)
        if family:
            return format_html(
                "<strong>{}</strong><br>"
                '<span style="color:var(--body-quiet-color); font-size:12px;">{}</span>',
                device,
                family,
            )
        return format_html("<strong>{}</strong>", device)

    @admin.display(description="Browser", ordering="browser")
    def browser_display(self, obj: LoginHistoryModel):
        browser = getattr(obj, "browser", None)
        if not browser:
            return format_html('<span style="opacity:.55;">{}</span>', "—")
        version = getattr(obj, "browser_version", None)
        if version:
            return format_html(
                "<strong>{}</strong> "
                '<span style="color:var(--body-quiet-color);">{}</span>',
                browser,
                version,
            )
        return format_html("<strong>{}</strong>", browser)

    @admin.display(description="Operating System", ordering="operating_system")
    def operating_system_display(self, obj: LoginHistoryModel):
        operating_system = getattr(obj, "operating_system", None)
        if not operating_system:
            return format_html('<span style="opacity:.55;">{}</span>', "—")
        version = getattr(obj, "operating_system_version", None)
        if version:
            return format_html(
                "<strong>{}</strong> "
                '<span style="color:var(--body-quiet-color);">{}</span>',
                operating_system,
                version,
            )
        return format_html("<strong>{}</strong>", operating_system)

    @admin.display(description="Location")
    def location_display(self, obj: LoginHistoryModel):
        city = getattr(obj, "city", None)
        region = getattr(obj, "region", None)
        country = getattr(obj, "country", None)
        country_code = getattr(obj, "country_code", None)

        if not any((city, region, country, country_code)):
            return format_html('<span style="opacity:.55;">{}</span>', "—")

        primary = city or region or country or country_code
        secondary = []
        if region and region != primary:
            secondary.append(region)
        if country and country != primary:
            secondary.append(country)
        if country_code:
            secondary.append(country_code.upper())

        if secondary:
            return format_html(
                "<strong>{}</strong><br>"
                '<span style="color:var(--body-quiet-color); font-size:12px;">{}</span>',
                primary,
                " • ".join(secondary),
            )
        return format_html("<strong>{}</strong>", primary)

    @admin.display(description="Coordinates")
    def coordinates_display(self, obj: LoginHistoryModel):
        latitude = getattr(obj, "latitude", None)
        longitude = getattr(obj, "longitude", None)
        if latitude is None or longitude is None:
            return format_html('<span style="opacity:.55;">{}</span>', "—")
        return format_html("<code>{}, {}</code>", latitude, longitude)

    @admin.display(description="User Agent")
    def user_agent_display(self, obj: LoginHistoryModel):
        user_agent = getattr(obj, "user_agent", None)
        if not user_agent:
            return format_html('<span style="opacity:.55;">{}</span>', "—")
        return format_html(
            '<div style="max-width:900px; overflow-wrap:anywhere; white-space:normal;"><code>{}</code></div>',
            user_agent,
        )

    @admin.display(description="Failure Reason")
    def failure_reason_display(self, obj: LoginHistoryModel):
        reason = getattr(obj, "failure_reason", None)
        if not reason:
            return format_html('<span style="opacity:.55;">{}</span>', "—")
        return format_html(
            '<div style="max-width:900px; overflow-wrap:anywhere; white-space:normal;"><code>{}</code></div>',
            reason,
        )

    @admin.display(description="Created", ordering="created_at")
    def created_at_display(self, obj: LoginHistoryModel):
        return obj.created_at
