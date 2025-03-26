# tasks/models.py
from django.db import models
from django.contrib.auth.models import User
from statuses.models import Status
from labels.models import Label

class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='tasks',  # Это создаст обратную связь status.tasks
        verbose_name='Статус',
        null=False,
        )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authored_tasks'
    )
    executor = models.ForeignKey(  # Изменили с assigned_to на executor
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='executed_tasks',
        verbose_name='Исполнитель'
    )
    labels = models.ManyToManyField(
        Label,
        related_name='tasks',
        blank=True,
        verbose_name='метки',)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
