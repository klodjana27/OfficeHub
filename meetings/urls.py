from django.urls import path
from .views import approve_booking, reject_booking, booking_list, request_meeting
from rest_framework.routers import DefaultRouter
from .views import RoomBookingViewSet

router = DefaultRouter()
router.register(r'room-bookings', RoomBookingViewSet, basename='room-booking')

urlpatterns = [
    path("", booking_list, name="meeting_list"),
    path("request/", request_meeting, name="request_meeting"),
    path("approve/<int:booking_id>/", approve_booking, name="approve_booking"),
    path("reject/<int:booking_id>/", reject_booking, name="reject_booking"),
]

urlpatterns += router.urls
