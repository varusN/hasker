from django.conf import settings
from django.urls import include, path
from user.views import (LoginView, LogOutView, PasswordChangeView,
                        SettingsView, SignUpView)

app_name = "site_auth"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout", LogOutView.as_view(), name="logout"),
    path("profile/", SettingsView.as_view(), name="profile"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("password/", PasswordChangeView.as_view(), name="password_change"),
]

if settings.DEBUG:
    urlpatterns.append(
        path("__debug__/", include("debug_toolbar.urls")),
    )
