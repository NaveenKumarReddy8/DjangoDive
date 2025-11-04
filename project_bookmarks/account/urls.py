from django.urls import path, include
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from account.views import user_login, dashboard, register, edit


urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("", include("django.contrib.auth.urls")),
    path("register/", register, name="register"),
    path("edit/", edit, name="edit"),
    # path("login/", user_login, name="login")
    # path("login/", LoginView.as_view(), name="login"),
    # path("logout/", LogoutView.as_view(), name="logout"),
    # path("password-change/", PasswordChangeView.as_view(), name="password_change"),
    # path(
    #     "password-change/done/",
    #     PasswordChangeDoneView.as_view(),
    #     name="password_change_done",
    # ),
    # path("password-reset/", PasswordResetView.as_view(), name="password_reset"),
    # path(
    #     "password-reset/done/",
    #     PasswordResetDoneView.as_view(),
    #     name="password_reset_done",
    # ),
    # path(
    #     "password-reset/<uidb64>/<token>/",
    #     PasswordResetConfirmView.as_view(),
    #     name="password_reset_confirm",
    # ),
    # path(
    #     "password-reset/complete/",
    #     PasswordResetCompleteView.as_view(),
    #     name="password_reset_complete",
    # ),
]
