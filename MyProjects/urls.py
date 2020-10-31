from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from tasks.api import TaskViewSet
from projects.api import ProjectViewSet
from notes.api import NoteViewSet
from .views import (MainPageView, ExportView, ImportView,
    ImportCompleteView, AboutSiteView)

router = DefaultRouter()
router.register('Task', TaskViewSet)
router.register('Project', ProjectViewSet)
router.register('Note', NoteViewSet)

urlpatterns = [
    path('export/', ExportView.as_view(), name='export'),
    path('import/', ImportView.as_view(), name='import'),
    path('import_complete/', ImportCompleteView.as_view(),
        name='import_complete'),
    path('about/', AboutSiteView.as_view(), name='about_site'),
    path('', MainPageView.as_view(), name='main'),
    path('admin/', admin.site.urls),
    path('api/get_token/', obtain_auth_token, name='get_token'),
    path('api/', include(router.urls)),
    path('project/', include('projects.urls')),
    path('account/', include('accounts.urls')),
    path('task/', include('tasks.urls')),
    path('notes/', include('notes.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
