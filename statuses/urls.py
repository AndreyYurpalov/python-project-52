# statuses/urls.py
from django.urls import path
from .views import StatusListView, StatusCreateView, StatusUpdateView, StatusDeleteView

urlpatterns = [
    path('statuses/', StatusListView.as_view(), name='status_list'),
    path('statuses/create/', StatusCreateView.as_view(), name='status_create'),
    path('statuses/<int:pk>/update/', StatusUpdateView.as_view(), name='status_update'),
    path('statuses/<int:pk>/delete/', StatusDeleteView.as_view(), name='status_delete'),
]