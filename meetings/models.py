from django.db import models
from django.contrib.auth import get_user_model

Employee = get_user_model()

class RoomBooking(models.Model):
    room = models.CharField(max_length=100, verbose_name="Room Name")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Employee")
    date = models.DateField(verbose_name="Booking Date")
    start_time = models.TimeField(verbose_name="Start Time")
    end_time = models.TimeField(verbose_name="End Time")
    description = models.TextField(blank=True, verbose_name="Description")  # ✅ Added description field
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")],
        default="Pending"
    )

    def __str__(self):
        return f"{self.room} - {self.date} ({self.start_time} - {self.end_time})"
