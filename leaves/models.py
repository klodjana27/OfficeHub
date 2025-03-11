from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta
from django.core.exceptions import ValidationError

Employee = get_user_model()

class LeaveBalance(models.Model):
    """ Ruajtja e bilancit të lejeve për çdo punonjës çdo vit """
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, verbose_name="Punonjësi", related_name="leave_balances"
    )
    year = models.IntegerField(verbose_name="Viti")
    total_leave_days = models.IntegerField(default=22, verbose_name="Ditë Leje Totale")
    custom_leave_days = models.IntegerField(default=22, verbose_name="Ditë Leje të Përcaktuara nga Admini")
    used_leave_days = models.IntegerField(default=0, verbose_name="Ditë Leje të Përdorura")

    class Meta:
        unique_together = ("employee", "year")

    def remaining_days(self):
        """ Llogarit ditët e mbetura të lejes """
        return max(0, self.custom_leave_days - self.used_leave_days)

    def __str__(self):
        return f"{self.employee.username} - {self.year} - {self.remaining_days()} ditë të mbetura"


class LeaveRequest(models.Model):
    """ Kërkesat për leje të punonjësve """
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, verbose_name="Punonjësi", related_name="leave_requests"
    )
    start_date = models.DateField(verbose_name="Data e Fillimit")
    end_date = models.DateField(verbose_name="Data e Mbarimit")
    
    leave_type = models.CharField(
        max_length=50,
        choices=[
            ("Annual", "Leje Vjetore"),
            ("Sick", "Leje Mjekësore"),
            ("Other", "Tjetër"),
        ],
        verbose_name="Lloji i Lejes"
    )
    
    status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Në Pritje"),
            ("Approved", "Aprovuar"),
            ("Rejected", "Refuzuar"),
        ],
        default="Pending",
        verbose_name="Statusi"
    )
    
    approved_by = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True, 
        related_name="approved_leaves", verbose_name="Aprovuar nga"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data e Krijimit")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data e Përditësimit")

    year = models.IntegerField(default=now().year, verbose_name="Viti")

    @property
    def duration(self):
        """ Llogarit numrin e ditëve të lejes """
        return (self.end_date - self.start_date).days + 1

    def clean(self):
        """ Siguron që data e mbarimit nuk është para datës së fillimit """
        if self.end_date < self.start_date:
            raise ValidationError("Data e mbarimit nuk mund të jetë para datës së fillimit.")

    def approve(self, approver):
        """ Approve a leave request and update leave balance correctly """
        leave_days = self.duration

        with transaction.atomic():
            balance, created = LeaveBalance.objects.get_or_create(
                employee=self.employee, year=self.year,
                defaults={"custom_leave_days": 22, "used_leave_days": 0}
            )

            # ✅ If the request was **previously approved**, restore the old balance before re-approving
            if self.status == "Approved":
                balance.used_leave_days -= leave_days
                balance.save()

            # ✅ Check if enough leave days are available
            if balance.remaining_days() < leave_days:
                raise ValidationError("Employee does not have enough remaining leave days.")

            # ✅ Deduct leave days and approve the request
            balance.used_leave_days += leave_days
            balance.save()

            self.status = "Approved"
            self.approved_by = approver
            self.save()

    def reject(self):
        """ Reject a leave request and restore leave balance if it was previously approved """
        
        with transaction.atomic():
            if self.status == "Approved":  # ✅ Only restore if previously approved
                balance = LeaveBalance.objects.get(employee=self.employee, year=self.year)
                balance.used_leave_days -= self.duration  # Restore used leave days
                balance.save()
                                   
            self.status = "Rejected"
            self.approved_by = None
            self.save()

    def __str__(self):
        return f"{self.employee.username} - {self.leave_type} ({self.status})"