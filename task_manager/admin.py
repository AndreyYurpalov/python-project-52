from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'format_date_joined', 'is_staff')

    def format_date_joined(self, obj):
        if obj.date_joined:
            # Преобразуем время в локальный часовой пояс и форматируем
            local_time = timezone.localtime(obj.date_joined)
            return local_time.strftime('%d.%m.%Y %H:%M')
        return "Нет данных"

    format_date_joined.short_description = 'Дата создания'  # Заголовок колонки
    format_date_joined.admin_order_field = 'date_joined'  # Сортировка по полю


# Регистрируем модель User с кастомным админ-классом
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)