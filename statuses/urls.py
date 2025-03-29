# statuses/urls.py
from django.urls import path
from .views import StatusListView, StatusCreateView, StstusUpdateView, StatusDeleteView

app_name = 'statuses'

urlpatterns = [
    path('', StatusListView.as_view(), name='list'),
    path('create/', StatusCreateView.as_view(), name='create'),
    path('<int:pk>/update/', StstusUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', StatusDeleteView.as_view(), name='delete'),
]