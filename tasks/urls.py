# tasks/urls.py
from django.urls import path
from .views import (
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskDetailView,
)

app_name = 'tasks'  # Это регистрирует namespace 'tasks'

urlpatterns = [
    path('', TaskListView.as_view(), name='list'),
    path('create/', TaskCreateView.as_view(), name='create'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='delete'),
    path('<int:pk>/', TaskDetailView.as_view(), name='detail'),
    ]
