from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminOld

from .models import User

@admin.register(User)
class UserAdmin(UserAdminOld):
    fieldsets = (
        (None, {'fields': ('username', 'avatar', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name',
                                                'email')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                      'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')})
    )
