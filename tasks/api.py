from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
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
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if int(request.data['creator']) != request.user.pk:
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
