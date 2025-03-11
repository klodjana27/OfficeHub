from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils.timezone import now
from .models import LeaveRequest, LeaveBalance

from users.models import Employee
from rest_framework import viewsets, permissions
from .serializers import LeaveRequestSerializer

### ✅ API për menaxhimin e lejeve me Django REST Framework
class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user, status="Pending")

### ✅ Shfaq të gjitha lejet e punonjësit të loguar
@login_required
def leave_requests_view(request):
    if request.user.role == "Manager" or request.user.role == "HR":
        leave_requests = LeaveRequest.objects.order_by("start_date")
    else:
        leave_requests = LeaveRequest.objects.filter(employee=request.user).order_by("start_date")
    
    print(request)
    return render(request, 'leaves/leave_requests_view.html', {
        'leave_requests': leave_requests,
        'user_role': request.user.role
    })

### ✅ Krijo një kërkesë të re për leje
@login_required
def request_leave(request):
    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        leave_type = request.POST.get("leave_type")

        #leave_days = (end_date - start_date).days + 1

        LeaveRequest.objects.create(
            employee=request.user,
            start_date=start_date,
            end_date=end_date,
            leave_type=leave_type,
            status="Pending"
        )
        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "error"}, status=400)

### ✅ Miratimi i një leje dhe përditësimi i bilancit
@login_required
def approve_leave(request, leave_id):
    leave_request = get_object_or_404(LeaveRequest, id=leave_id)

    if request.user.role in ["Manager", "HR"]:
        leave_request.status = "Approved"
        leave_request.approved_by = request.user
        leave_request.save()

        balance, _ = LeaveBalance.objects.get_or_create(
            employee=leave_request.employee, year=leave_request.year
        )

        if balance.remaining_days() >= leave_request.duration:
            balance.used_leave_days += leave_request.duration
            balance.save()
        else:
            return JsonResponse({"error": "Punonjësi nuk ka mjaftueshëm ditë leje të mbetura."}, status=400)

        return JsonResponse({"message": "Leja u aprovua me sukses!"})

    return JsonResponse({"error": "Nuk keni leje për të aprovuar këtë kërkesë"}, status=403)

### ✅ Refuzimi i një leje
@login_required
def reject_leave(request, leave_id):
    leave_request = get_object_or_404(LeaveRequest, id=leave_id)

    if request.user.role in ["Manager", "HR"]:
        if leave_request.status == "Approved":
            balance, _ = LeaveBalance.objects.get_or_create(
            employee=leave_request.employee, year=leave_request.year
            )
            balance.used_leave_days -= leave_request.duration
            balance.save()
        leave_request.status = "Rejected"
        
        leave_request.approved_by = None
        leave_request.save()
        return JsonResponse({"message": "Leja u refuzua me sukses!"})

    return JsonResponse({"error": "Nuk keni leje për të refuzuar këtë kërkesë"}, status=403)

### ✅ Përmbledhje e lejeve të punonjësit
@login_required
def leave_summary_view(request):
    employee = request.user
    current_year = now().year
    current_balance, _ = LeaveBalance.objects.get_or_create(employee=employee, year=current_year)

    context = {
        "current_balance": current_balance,
        "leave_history": LeaveRequest.objects.filter(employee=employee, status="Approved").order_by("-start_date"),
    }
    return render(request, "leaves/leave_summary_view.html", context)

### ✅ API për të shfaqur sa leje ka mbetur
@login_required
def remaining_leaves_api(request):
    employee = request.user
    current_year = now().year
    balance, _ = LeaveBalance.objects.get_or_create(employee=employee, year=current_year)
    return JsonResponse({"remaining_leaves": balance.remaining_days()})

