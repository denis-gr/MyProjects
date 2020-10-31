from django.db.models import (
    Model, CharField, DateTimeField, DateField, TextField, ForeignKey, CASCADE
)
from django.utils import timezone
from django.contrib.auth import get_user_model

from projects.models import Project

User = get_user_model()

class Task(Model):
    name = CharField('Название', max_length=150)
    start = DateTimeField('Начат', default=timezone.now)
    end = DateTimeField('Окончен', blank=True, null=True)
    soft_deadline = DateField('Мягкий дедлайн', blank=True, null=True)
    hard_deadline = DateField('Жесткий дедлайн', blank=True, null=True)
    description = TextField('Описание', blank=True)
    project = ForeignKey(
        Project,
        verbose_name='Проект',
        on_delete=CASCADE,
        blank=True,
        null=True,
    )
    creator = ForeignKey(User, verbose_name='Создатель', on_delete=CASCADE)

    def resume(self):
        self.end = None
        self.save()

    def complete(self):
        self.end = timezone.now()
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
