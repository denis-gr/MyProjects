from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import User

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = "username", "email"
        model = User


class UserDetailForm(ModelForm):
    class Meta:
        model = User
        fields = 'username', 'first_name', 'last_name', 'email',
