from django.contrib import admin
from django.utils.html import format_html

from accounts.models import UserAvatarModel


@admin.register(UserAvatarModel)
class UserAvatarAdmin(admin.ModelAdmin):
    """
    Admin configuration for user avatars.
    """

    list_per_page = 50

    list_display = (
        "user",
        "is_primary",
        "created_at",
        "thumbnail",
    )

    list_display_links = (
        "thumbnail",
        "user",
    )

    list_filter = (
        "is_primary",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "user__phone_number",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "id",
        "preview",
        "created_at",
    )

    autocomplete_fields = ("user",)

    fieldsets = (
        (
            "Avatar",
            {
                "fields": (
                    "id",
                    "user",
                    "image",
                    "preview",
                    "is_primary",
                ),
            },
        ),
        (
            "Dates",
            {
                "fields": ("created_at",),
            },
        ),
    )

    def get_queryset(self, request):
        """
        Optimize avatar list query.
        """

        queryset = super().get_queryset(request)

        return queryset.select_related(
            "user",
        )

    @admin.display(description="Avatar")
    def thumbnail(self, obj):
        """
        Display avatar thumbnail.
        """

        if not obj.image:
            return "-"

        return format_html(
            '<img src="{}" width="48" height="48" '
            'style="border-radius:50%;object-fit:cover;" />',
            obj.image.url,
        )

    @admin.display(description="Preview")
    def preview(self, obj):
        """
        Display large avatar preview.
        """

        if not obj.pk or not obj.image:
            return "-"

        return format_html(
            '<img src="{}" width="200" ' 'style="border-radius:8px;max-width:100%;" />',
            obj.image.url,
        )
