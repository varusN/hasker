from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import \
    AuthenticationForm as AuthenticationFormGeneric
from django.contrib.auth.forms import UserChangeForm as UserChangeFormGeneric
from django.contrib.auth.forms import \
    UserCreationForm as UserCreationFormGeneric


class AuthenticationForm(AuthenticationFormGeneric):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field: forms.Field
            widget: forms.Widget = field.widget
            widget.attrs["class"] = "form-control"


class UserCreationForm(UserCreationFormGeneric):
    class Meta(UserCreationFormGeneric.Meta):
        model = get_user_model()
        fields = ("username", "email", "photo", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field: forms.Field
            widget: forms.Widget = field.widget
            widget.attrs["class"] = "form-control"


class SettingsForm(UserChangeFormGeneric):
    password = None

    class Meta:
        model = get_user_model()
        fields = ("email", "photo")
