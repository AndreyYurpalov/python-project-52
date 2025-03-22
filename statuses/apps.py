# statuses/apps.py
from django.apps import AppConfig

class StatusesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'statuses'  # Убедитесь, что имя приложения указано правильно
