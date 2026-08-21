from django.contrib import admin
from django.conf import settings
from rest_framework import routers
from django.urls import path, include
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from .app_config import config

router = routers.DefaultRouter()

base_url = config.app.base_url
admin_url = config.app.admin_url

urlpatterns = [
    path("", include("core.api.urls")),
    path(base_url, include(router.urls)),
    # Admin URL without base_url
    path(base_url + admin_url, admin.site.urls),
    # API documentation
    path(
        "schema/",
        SpectacularAPIView.as_view(api_version="v1"),
        name="schema-v1",
    ),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema-v1"),
    ),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="schema-v1"),
        name="redoc-v1",
    ),
    # API v1 routes
    path(base_url + "v1/accounts/", include("accounts.api.v1.urls")),
    path(base_url + "v1/authentication/", include("authentication.api.v1.urls")),
]


if settings.DEBUG:
    urlpatterns += (path("__debug__/", include("debug_toolbar.urls")),)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.index_title = f"{config.app.app_name} Admin"
admin.site.site_header = f"{config.app.app_name} Admin"
admin.site.site_title = f"{config.app.app_name}"
