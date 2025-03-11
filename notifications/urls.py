from django.urls import path
from . import views  # Importimi i sigurt

urlpatterns = [
    path('', views.notifications_view, name='notifications'),
]
