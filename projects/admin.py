from django.contrib import admin

from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'description',)}),
        ('Дедлайны', {'fields': ('soft_deadline', 'hard_deadline')}),
        ('Важные моменты', {'fields': ('start', 'end')}),
    )
    list_display = 'name',
    search_fields = 'name', 'description'
