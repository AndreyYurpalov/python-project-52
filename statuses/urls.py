# statuses/urls.py
from django.urls import path
from . import views

app_name = 'statuses'

urlpatterns = [
    path('', views.status_list, name='list'),
    path('create/', views.status_create, name='create'),
    path('<int:pk>/update/', views.status_update, name='update'),
    path('<int:pk>/delete/', views.status_delete, name='delete'),
]