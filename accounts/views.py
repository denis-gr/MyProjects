from django.views.generic import CreateView, UpdateView
from django.views.generic.base import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib.auth.views import LoginView as OldLoginView

from .models import User
from .forms import SignUpForm, UserDetailForm, LoginForm

class LoginView(OldLoginView):
    form_class = LoginForm


class SignUpView(CreateView):
    template_name = 'accounts/sign_up.html'
    form_class = SignUpForm
    model = User
    success_url = settings.LOGIN_URL


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserDetailForm
    success_url = settings.PROFILE_PAGE_URL
    template_name = 'accounts/profile.html'

    def get_object(self, queryset=None):
        return self.request.user


class UserDeleteView(LoginRequiredMixin, RedirectView):
    url = settings.MAIN_PAGE_URL

    def get(self, request, *args, **kwargs):
        user = request.user
        user.is_active = False
        user.save()
        return super().get(request, *args, **kwargs)
  
