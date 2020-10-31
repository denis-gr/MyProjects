from django.contrib.auth import get_user_model
from django.db.models import (CASCADE, CharField, DateTimeField, ForeignKey,
                              DateField, Model, TextField)
from django.shortcuts import reverse
from django.utils import timezone


User = get_user_model()


class Project(Model):
    name = CharField('Название', max_length=150)
    start = DateTimeField('Начат', default=timezone.now)
    end = DateTimeField('Окончен', blank=True, null=True)
    soft_deadline = DateField('Мягкий дедлайн', blank=True, null=True)
    hard_deadline = DateField('Жесткий дедлайн', blank=True, null=True)
    description = TextField('Описание', blank=True)
    creator = ForeignKey(User, verbose_name='Создатель', on_delete=CASCADE)

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'pk': self.pk})

    def resume(self):
        self.end = None
        self.save()

    def complete(self):
        self.end = timezone.now()
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
