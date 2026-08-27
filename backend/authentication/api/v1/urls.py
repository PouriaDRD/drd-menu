from django.urls import path

from .views import (
    LoginAPIView,
    LogoutView,
    TokenRefreshAPIView,
    LoginHistoryAPIView,
)

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", TokenRefreshAPIView.as_view(), name="refresh"),
    path("login-history/", LoginHistoryAPIView.as_view(), name="login-history"),
]
