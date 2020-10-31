from rest_framework.authtoken.models import Token
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Note

def get_token(user):
    return Token.objects.get_or_create(user=user)[0].key


class NoteView(LoginRequiredMixin, ListView):
    model = Note

    def get_context_data(self, **kwargs):
        kwargs['token'] = get_token(self.request.user)
        return super().get_context_data(**kwargs)
