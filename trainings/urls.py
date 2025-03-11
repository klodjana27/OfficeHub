from django.urls import path
from .views import training_list  # Sigurohu që ky funksion ekziston te views.py

urlpatterns = [
    path('', training_list, name='training_list'),
]
