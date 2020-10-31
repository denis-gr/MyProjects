from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from rest_framework.authtoken.models import Token

from .models import Project
from .forms import ProjectForm

def get_token(user):
    return Token.objects.get_or_create(user=user)[0].key


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    template_name_suffix = '_update'
    fields = 'name', 'soft_deadline', 'hard_deadline', 'description'

    def get_context_data(self, **kwargs):
        kwargs['token'] = get_token(self.request.user)
        return super().get_context_data(**kwargs)


class ProjectListView(LoginRequiredMixin, ListView):
    template_name = 'projects/project_list.html'
    model = Project

    ORGANIZING_ACTIONS = {
        'name_up': lambda queryset: queryset.order_by('-name'),
        'name_down': lambda queryset: queryset.order_by('name'),
        'start_up': lambda queryset: queryset.order_by('-start'),
        'start_down': lambda queryset: queryset.order_by('start'),
    }

    def get_queryset(self):
        objects = super().get_queryset().filter(creator=self.request.user)

        if 'ordering' in self.request.GET and self.request.GET['ordering']:
            ordering = self.request.GET['ordering']
            objects = self.ORGANIZING_ACTIONS[ordering](objects)

        if 'search' in self.request.GET and self.request.GET['search']:
            s = self.request.GET['search']
            objects = objects.filter(Q(name__icontains=s) | Q(description__icontains=s))

        return objects


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = '/project/'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
