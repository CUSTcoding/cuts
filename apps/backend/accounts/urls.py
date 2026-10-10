
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView,
    MeView,
    LogoutView,
    ChangePasswordView,
    ForgotPasswordView,
    ResetPasswordView,
)
from .views import LoginView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("me/", MeView.as_view(), name="me"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change_password",
    ),
    path(
        "forgot-password/",
        ForgotPasswordView.as_view(),
        name="forgot_password",
    ),
    path(
        "reset-password/",
        ResetPasswordView.as_view(),
        name="reset_password",
    ),
]