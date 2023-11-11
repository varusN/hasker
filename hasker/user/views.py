from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.views import (
    LoginView as LoginViewGeneric,
    LogoutView as LogoutViewGeneric,
)
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from .forms import AuthenticationForm, UserCreationForm


class LoginView(LoginViewGeneric):
    template_name = "user/login.html"
    form_class = AuthenticationForm
    next_page = reverse_lazy("site_auth:profile")


class LogOutView(LogoutViewGeneric):
    next_page = reverse_lazy("site_auth:profile")


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "user/register.html"
    success_url = reverse_lazy("site_auth:profile")

    def form_valid(self, form):
        print('CASDADASDAS')
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


def error_403_csrf_failure(request, reason=""):
    if request.path == '/user/login/' and request.user.is_authenticated:
        next = request.GET.get('next', '/')
        return HttpResponseRedirect(next)

    url = reverse('login') + '?next=' + request.path
    context = {
        'page_title': "Authentication Error",
        'continue_url': url,
        'reason': reason,
    }
    response = render(request, "base/403_csrf.html", context=context)
    response.status_code = 403
    return response