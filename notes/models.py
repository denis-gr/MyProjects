from django.contrib.auth import get_user_model
from django.db.models import CASCADE, ForeignKey, Model, TextField

from projects.models import Project

User = get_user_model()

class Note(Model):
    text = TextField('Текст')
    project = ForeignKey(
        Project,
        verbose_name='Проект',
        on_delete=CASCADE,
        blank=True,
        null=True,
    )
    creator = ForeignKey(User, verbose_name='Создатель', on_delete=CASCADE)

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'

    def __str__(self):
        return self.text
