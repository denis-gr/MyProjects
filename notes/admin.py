from django.contrib import admin

from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    fields = 'text', 'creator', 'project'
    list_display = 'text',
    search_fields = 'text',
