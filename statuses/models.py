# statuses/models.py
from django.db import models

class Status(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='status_name')

    def __str__(self):
        return self.name