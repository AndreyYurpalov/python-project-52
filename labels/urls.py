from django.urls import path

from .views import LabelListView, LabelCreatedView, LabelUpdateView, LabelDeleteView

app_name = 'labels'

urlpatterns = [
    path('', LabelListView.as_view(), name='list'),
    path('create/', LabelCreatedView.as_view(), name='create'),
    path('<int:pk>/update/', LabelUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', LabelDeleteView.as_view(), name='delete'),
]
