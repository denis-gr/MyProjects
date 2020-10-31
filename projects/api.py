from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Project
from .serializers import ProjectSerializer
from tasks.models import Task
from notes.models import Note

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['text']

    def create(self, request, *args, **kwargs):
        if int(request.data['creator']) != request.user.pk:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(creator=self.request.user)

    def destroy(self, request, *args, **kwargs):
        if self.get_object().creator.pk != request.user.pk:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if self.get_object().creator.pk != request.user.pk:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    @action(methods=['PATCH'], detail=True)
    def resume(self, request, pk=None):
        if self.get_object().creator.pk != request.user.pk:
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.get_object().resume()
        return self.retrieve(self, request)

    @action(methods=['PATCH', 'GET'], detail=True)
    def complete(self, request, pk=None):
        if self.get_object().creator.pk != request.user.pk:
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.get_object().complete()
        return self.retrieve(self, request)

    @action(methods=['GET'], detail=True)
    def get_notes(self, request, pk=None):
        if self.get_object().creator.pk != request.user.pk:
            return Response(status=status.HTTP_403_FORBIDDEN)
        notes = Note.objects.filter(project=self.get_object())
        notes = list(map(lambda x: x.pk, notes))
        return Response(notes)

    @action(methods=['PATCH'], detail=True)
    def add_note(self, request, pk=None):
        if self.get_object().creator.pk != request.user.pk:
            return Response(status=status.HTTP_403_FORBIDDEN)
        data = request.data
        data['creator'] = request.user
        data['project'] = self.get_object()
        Note.objects.create(**request.data)
        return self.retrieve(self, request)

    @action(methods=['DELETE'], detail=True)
    def delete_note(self, request, pk=None):
        if int(request.data['creator']) != request.user.pk:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if 'pk' in request.data:
            pk = request.data['pk']
        elif 'id' in request.data:
            pk = request.data['id']
        Note.objects.get(pk=pk).delete()
        return self.retrieve(self, request)

    @action(methods=['GET'], detail=True)
    def get_tasks(self, request, pk=None):
        if self.get_object().creator.pk != request.user.pk:
            return Response(status=status.HTTP_403_FORBIDDEN)
        tasks = Task.objects.filter(project=self.get_object())
        tasks = list(map(lambda x: x.pk, tasks))
        return Response(tasks)

    @action(methods=['PATCH', 'GET'], detail=True)
    def add_task(self, request, pk=None):
        if self.get_object().creator.pk != request.user.pk:
            return Response(status=status.HTTP_403_FORBIDDEN)
        data = request.data
        data['creator'] = request.user
        data['project'] = self.get_object()
        Task.objects.create(**request.data)
        return self.retrieve(self, request)

    @action(methods=['DELETE'], detail=True)
    def delete_task(self, request, pk=None):
        if int(request.data['creator']) != request.user.pk:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if 'pk' in request.data:
            pk = request.data['pk']
        elif 'id' in request.data:
            pk = request.data['id']
        Task.objects.get(pk=pk).delete()
        return self.retrieve(self, request)
