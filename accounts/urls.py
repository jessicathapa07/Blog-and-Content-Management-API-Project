from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterAPIView,
    LoginAPIView,
    ProfileAPIView,
    ChangePasswordAPIView,
)

urlpatterns = [
    # Authentication
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("signup/", RegisterAPIView.as_view(), name="signup"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # User Profile
    path("profile/", ProfileAPIView.as_view(), name="profile"),

    # Change Password
    path("change-password/", ChangePasswordAPIView.as_view(), name="change_password"),
]