from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    leave_requests_view, 
    request_leave, 
    approve_leave, 
    reject_leave, 
    leave_summary_view, 
    remaining_leaves_api
)
from django.http import JsonResponse

# ✅ Regjistrojmë API në një router
# router = DefaultRouter()
# router.register(r'api', LeaveRequestViewSet)  # API do të jetë në /leaves/api/


# ✅ Definojmë `urlpatterns`
urlpatterns = [
    path('leave_requests/', leave_requests_view, name='leave_requests'),  # Faqja kryesore për lejet
    path('request/', request_leave, name='request_leave'),  # Kërkesa për leje
    path('approve/<int:leave_id>/', approve_leave, name='approve_leave'),  # Miratimi i lejes
    path('reject/<int:leave_id>/', reject_leave, name='reject_leave'),  # Refuzimi i lejes
    path('summary/', leave_summary_view, name='leave_summary'),  # Përmbledhja e lejeve
    path('remaining/', remaining_leaves_api, name='remaining_leaves_api'),  # API për lejet e mbetura
  #  path('api/', include(router.urls)),  # ✅ Përfshijmë API-n
   
]
