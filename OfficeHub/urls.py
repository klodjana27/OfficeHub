"""
URL configuration for OfficeHub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.views.generic import RedirectView
from django.conf import settings
from django.urls import path, include
from django.http import JsonResponse
from django.contrib import admin
from django.contrib.auth import views as auth_views  

def home(request):
    return JsonResponse({"message": "Welcome to OfficeHub API!"})

urlpatterns = [
    path('', home),  # Mesazhi në faqen kryesore
    path('admin/', admin.site.urls),
    #path('', include('users.urls')),
    path('leaves/', include('leaves.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('users/', include('users.urls')),
    path('meetings/', include('meetings.urls')),
    path('trainings/', include('trainings.urls')),
    path('notifications/', include('notifications.urls')),
    
    # ✅ Rregullon problemin e favicon.ico
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico', permanent=True)),
]
