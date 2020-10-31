from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminOld

from .models import User

from .forms import UserChangeForm, UserCreationForm

@admin.register(User)
class UserAdmin(UserAdminOld):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                      'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')})
    )
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)