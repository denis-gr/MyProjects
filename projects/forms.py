from django.forms import ModelForm

from .models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = 'creator', 'start', 'end',
