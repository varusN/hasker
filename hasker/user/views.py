from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.views import LoginView as LoginViewGeneric
from django.contrib.auth.views import LogoutView as LogoutViewGeneric
from django.contrib.auth.views import \
    PasswordChangeView as PasswordChangeViewGeneric
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from user.forms import AuthenticationForm, SettingsForm, UserCreationForm


class PasswordChangeView(PasswordChangeViewGeneric):
    template_name = "user/change_password.html"
    form_class = PasswordChangeForm
    success_url = reverse_lazy("question:index")


class LoginView(LoginViewGeneric):
    template_name = "user/login.html"
    form_class = AuthenticationForm
    next_page = reverse_lazy("site_auth:profile")


class LogOutView(LogoutViewGeneric):
    next_page = reverse_lazy("question:index")


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "user/register.html"
    success_url = reverse_lazy("question:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        # user: AbstractUser = self.object
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user: AbstractUser = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response


class SettingsView(UpdateView):
    form_class = SettingsForm
    success_url = reverse_lazy("site_auth:profile")
    template_name = "user/profile.html"

    def form_valid(self, *args, **kwargs):
        messages.success(self.request, "Your settings have been successfully updated!")
        return super().form_valid(*args, **kwargs)

    def form_invalid(self, *args, **kwargs):
        self.object.refresh_from_db()
        return super().form_invalid(*args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user
