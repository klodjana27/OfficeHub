from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.timezone import now
from rest_framework import viewsets, permissions
from .models import RoomBooking
from .serializers import RoomBookingSerializer  # Make sure this import exists




from datetime import datetime

### ✅ API ViewSet for Room Bookings
class RoomBookingViewSet(viewsets.ModelViewSet):
    queryset = RoomBooking.objects.all()
    serializer_class = RoomBookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """ When an employee requests a new booking, set status to Pending """
        serializer.save(employee=self.request.user, status="Pending")

### ✅ List all bookings
@login_required
def booking_list(request):
    """ Display all room bookings """
    bookings = RoomBooking.objects.all().order_by("-date", "-start_time")
    is_coordinator = request.user.is_superuser or request.user.groups.filter(name="Coordinator").exists()

    return render(request, "meetings/room_bookings.html", {
        "bookings": bookings,
        "is_coordinator": is_coordinator
    })


@login_required
def request_meeting(request):
    if request.method == "POST":
        room = request.POST.get("room")
        date_str = request.POST.get("date")
        start_time_str = request.POST.get("start_time")
        end_time_str = request.POST.get("end_time")
        description = request.POST.get("description", "")  # ✅ Ensure description is captured

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            start_time = datetime.strptime(start_time_str, "%H:%M").time()
            end_time = datetime.strptime(end_time_str, "%H:%M").time()
        except ValueError:
            return JsonResponse({"status": "error", "message": "Invalid date or time format"}, status=400)

        # ✅ Create RoomBooking instance with description
        RoomBooking.objects.create(
            room=room,
            employee=request.user,
            date=date,
            start_time=start_time,
            end_time=end_time,
            description=description,  # ✅ Ensure this is included
            status="Pending"
        )
        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "error"}, status=400)


from django.http import JsonResponse

@login_required
def approve_booking(request, booking_id):
    """ Coordinator approves a meeting room booking """
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    booking = get_object_or_404(RoomBooking, id=booking_id)

    if request.user.is_superuser or request.user.groups.filter(name="Coordinator").exists():
        booking.status = "Approved"
        booking.coordinator = request.user
        booking.save()
        return JsonResponse({"message": "Rezervimi i sallës u aprovua me sukses!"})
    
    return JsonResponse({"error": "Nuk keni leje për të aprovuar këtë rezervim"}, status=403)

@login_required
def reject_booking(request, booking_id):
    """ Coordinator rejects a meeting room booking """
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    booking = get_object_or_404(RoomBooking, id=booking_id)

    if request.user.is_superuser or request.user.groups.filter(name="Coordinator").exists():
        booking.status = "Rejected"
        booking.coordinator = None
        booking.save()
        return JsonResponse({"message": "Rezervimi i sallës u refuzua me sukses!"})
    
    return JsonResponse({"error": "Nuk keni leje për të refuzuar këtë rezervim"}, status=403)


