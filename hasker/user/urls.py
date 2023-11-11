from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic import TemplateView

from user.views import LoginView, SignUpView, LogOutView

app_name="site_auth"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout", LogOutView.as_view(), name="logout"),
    path("profile/", TemplateView.as_view(template_name="user/profile.html"), name="profile"),
    path("signup/", SignUpView.as_view(), name="signup"),
]

if settings.DEBUG:
    urlpatterns.append(
    path("__debug__/", include("debug_toolbar.urls")),
    )