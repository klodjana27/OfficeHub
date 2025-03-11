from django.contrib import admin
from .models import LeaveRequest, LeaveBalance

@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = ("employee", "year", "custom_leave_days", "used_leave_days", "remaining_days")
    list_editable = ("custom_leave_days",)  # ✅ Lejon Office Admin të ndryshojë ditët e lejes
    list_filter = ("year", "employee")
    search_fields = ("employee__username", "year")

    def remaining_days(self, obj):
        return obj.remaining_days()

    remaining_days.short_description = "Ditë të Mbetura"


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ("employee", "start_date", "end_date", "leave_type", "status", "approved_by")
    list_filter = ("status", "leave_type", "year")
    search_fields = ("employee__username", "status")
