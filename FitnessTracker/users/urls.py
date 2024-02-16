from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.UserLogin.as_view(), name="login"),
    path("logout/", views.UserLogout.as_view(), name="logout"),
    path("registration/", views.Registration.as_view(), name="registration"),
    path("activate/<uidb64>/<token>/", views.ActivateView.as_view(), name="activate"),
    path(
        "change_password/",
        views.ChangePasswordView.as_view(),
        name="change_password",
    ),
    path("reset_password/", views.ResetPasswordView.as_view(), name="reset_password"),
    path(
        "reset_password/<uidb64>/<token>/",
        views.ResetPasswordConfirmView.as_view(),
        name="reset_password_confirm_token",
    ),
    path(
        "reset_password_confirm/",
        views.ResetPasswordConfirmView.as_view(),
        name="reset_password_confirm",
    ),
    path("settings/", views.SettingsView.as_view(), name="settings"),
]
