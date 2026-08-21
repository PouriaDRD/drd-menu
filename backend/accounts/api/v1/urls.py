from django.urls import path

from .views import (
    UserProfileAPIView,
    UserProfileUpdateAPIView,
)

urlpatterns = [
    path("my-profile/", UserProfileAPIView.as_view(), name="user-profile"),
    path(
        "my-profile/update/",
        UserProfileUpdateAPIView.as_view(),
        name="user-profile-update",
    ),
]
