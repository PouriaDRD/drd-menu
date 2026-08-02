from django.contrib import admin
from django.utils.html import format_html

from accounts.models import UserAvatarModel


class UserAvatarInline(admin.TabularInline):
    """
    Inline admin for managing user avatars.
    """

    model = UserAvatarModel

    extra = 1

    fields = (
        "preview",
        "image",
        "is_primary",
        "created_at",
    )

    readonly_fields = (
        "preview",
        "created_at",
    )

    ordering = ("-created_at",)

    def get_queryset(self, request):
        """
        Optimize inline queryset.
        """

        queryset = super().get_queryset(request)

        return queryset.select_related(
            "user",
        )

    @admin.display(description="Preview")
    def preview(self, obj):
        """
        Display avatar preview.
        """

        if not obj.pk or not obj.image:
            return "-"

        return format_html(
            '<img src="{}" width="60" height="60" '
            'style="border-radius:50%;object-fit:cover;" />',
            obj.image.url,
        )

    def save_formset(self, request, form, formset, change):
        """
        Ensure only one primary avatar per user.
        """

        instances = formset.save(commit=False)

        for instance in instances:
            instance.save()

            if instance.is_primary:
                (
                    UserAvatarModel.objects.filter(
                        user=instance.user,
                        is_primary=True,
                    )
                    .exclude(
                        pk=instance.pk,
                    )
                    .update(
                        is_primary=False,
                    )
                )

        formset.save_m2m()
