from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'description', 'creator', 'project')}),
        ('Дедлайны', {'fields': ('soft_deadline', 'hard_deadline')}),
        ('Важные моменты', {'fields': ('start', 'end')}),
    )
    list_display = 'name',
    search_fields = 'name', 'description'
    ordering = 'name',
