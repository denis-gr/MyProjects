from django.forms import Form, ModelForm, EmailField
from django.contrib.auth import authenticate
from django.utils.text import capfirst
from django.contrib.auth.forms import (UserCreationForm,
    UserChangeForm as OldUserChangeForm, AuthenticationForm)

from .models import User

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = "email",
        model = User


class UserDetailForm(ModelForm):
    class Meta:
        model = User
        fields = 'email',


class UserChangeForm(OldUserChangeForm):
    class Meta:
        model = User
        fields = ('email',)


class LoginForm(AuthenticationForm):
    username = None
    email = EmailField()

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(Form, self).__init__(*args, **kwargs)

        self.username_field = User._meta.get_field(User.USERNAME_FIELD)
        if self.fields['email'].label is None:
            self.fields['email'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
