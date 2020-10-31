import json
import os

from django.views.generic import TemplateView, FormView
from django.forms import Form, BooleanField
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.conf import settings

from projects.models import Project
from projects.serializers import ProjectSerializer
from tasks.models import Task
from tasks.serializers import TaskSerializer
from notes.models import Note
from notes.serializers import NoteSerializer

class MainPageView(TemplateView):
    template_name = 'main.html'


class AboutSiteView(TemplateView):
    template_name = 'about_site.html'


class ExportView(LoginRequiredMixin, FormView):
    template_name = "export.html"

    def get_form_class(self):
        data = {}

        for project in Project.objects.filter(creator=self.request.user):
            data[f"project_{project.pk}"] = BooleanField(
                label=project.name, required=False)

        for task in Task.objects.filter(creator=self.request.user):
            data[f"task_{task.pk}"] = BooleanField(
                label=task.name, required=False)

        for note in Note.objects.filter(creator=self.request.user):
            data[f"note_{note.pk}"] = BooleanField(
                label=note.text[:50], required=False)

        return type("NewForm", (Form,), data)     

    def form_valid(self, form):
        user = self.request.user
        data = {}
        ids = { "project": set(), "task": set(), "note": set() }

        for field in form:
            t, pk = field.name.split("_")
            if field.value():
                ids[t].add(pk)

        data["projects"] = [ProjectSerializer(i).data for i in
            Project.objects.filter(creator=user, pk__in=ids["project"])]
        for i in data["projects"]:
            del i["creator"]

        data["tasks"] = [TaskSerializer(i).data for i in
            Task.objects.filter(creator=user, pk__in=ids["task"])]
        for i in data["tasks"]:
            del i["creator"]

        data["notes"] = [NoteSerializer(i).data for i in
            Note.objects.filter(creator=user, pk__in=ids["note"])]
        for i in data["notes"]:
            del i["creator"]

        response = HttpResponse(json.dumps(data))
        response['Content-Type'] = "application/octet-stream"
        response['Content-Disposition'] = 'inline; filename=export.json'
        return response


class ImportView(LoginRequiredMixin, FormView):
    form_class = Form
    success_url = reverse_lazy("import_complete")
    template_name = "import.html"

    def form_valid(self, form):
        url = f"temp/import_{self.request.user.pk}.json"
        path = os.path.join(settings.MEDIA_ROOT, url)
        with self.request.FILES['file'] as f1, open(path, "w") as f2:
            f2.write(f1.open().read().decode())
        return super().form_valid(form)


class ImportCompleteView(LoginRequiredMixin, FormView):
    success_url = reverse_lazy("profile")
    template_name = "import_complete.html"

    def get_form_class(self):
        url = f"temp/import_{self.request.user.pk}.json"
        path = os.path.join(settings.MEDIA_ROOT, url)
        fields = {}
        with open(path) as f:
            data = json.load(f)

        for project in data["projects"]:
            fields[f"project_{project['id']}"] = BooleanField(
                label=project["name"], required=False)

        for task in data["tasks"]:
            fields[f"task_{task['id']}"] = BooleanField(
                label=task["name"], required=False)

        for note in data["notes"]:
            fields[f"note_{note['id']}"] = BooleanField(
                label=note["text"][:39], required=False)
        return type("NewForm", (Form,), fields)  

    def form_valid(self, form):
        url = f"temp/import_{self.request.user.pk}.json"
        path = os.path.join(settings.MEDIA_ROOT, url)
        with open(path) as f:
            data = json.load(f)
        os.remove(path)

        Project.objects.filter(creator=self.request.user).delete()
        Task.objects.filter(creator=self.request.user).delete()
        Note.objects.filter(creator=self.request.user).delete()

        projects = {}
        for project in data["projects"]:
            if form[f"project_{project['id']}"].value():
                old_id = project["id"]
                del project["id"]
                project["creator"] = self.request.user
                projects[old_id] = Project.objects.create(**project)

        for task in data["tasks"]:
            if form[f"task_{task['id']}"].value():
                task["creator"] = self.request.user
                if task["project"]:
                    task["project"] = projects[task["project"]]
                Task.objects.create(**task)

        for note in data["notes"]:
            if form[f"note_{note['id']}"].value():
                note["creator"] = self.request.user
                if note["project"]:
                    note["project"] = projects[note["project"]]
                Note.objects.create(**note)
        return super().form_valid(form)             
