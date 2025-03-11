from rest_framework import serializers
from .models import LeaveRequest

class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_username = serializers.CharField(source='employee.username', read_only=True)

    class Meta:
        model = LeaveRequest
        fields = ['id', 'employee_username', 'start_date', 'end_date', 'leave_type', 'status', 'approved_by']
