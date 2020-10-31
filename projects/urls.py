from django.urls import path

from .views import (ProjectCreateView, ProjectListView,
    ProjectUpdateView, ProjectDeleteView)

urlpatterns = [
    path(
        '<int:pk>/delete/',
        ProjectDeleteView.as_view(),
        name='project_delete'),
    path('<int:pk>/', ProjectUpdateView.as_view(), name='project_detail'),
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('', ProjectListView.as_view(), name='project_list'),
]
