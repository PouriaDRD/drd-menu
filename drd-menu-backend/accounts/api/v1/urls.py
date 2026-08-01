from django.urls import path

from .views import (
    UserProfileAPIView,
)

urlpatterns = [
    path("my-profile/", UserProfileAPIView.as_view(), name="user-profile"),
]
