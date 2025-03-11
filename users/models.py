from django.contrib.auth.models import AbstractUser
from django.db import models

class Department(models.Model):
    """Model për Departamentet në kompani"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Position(models.Model):
    """Model për Pozicionet e Punës"""
    name = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="positions")

    def __str__(self):
        return f"{self.name} ({self.department.name})"

class Employee(AbstractUser):
    """Modeli i personalizuar i përdoruesit (punonjësit)"""
    
    ROLE_CHOICES = [
        ('CEO', 'CEO'),
        ('HR', 'Human Resources'),
        ('Coordinator', 'Coordinator'),
        ('Office Admin', 'Office Admin'),
        ('Manager', 'Manager'),
        ('Employee', 'Employee'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Employee')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")

    # Mbikëqyrësi i drejtpërdrejtë (p.sh., menaxheri i punonjësit)
    supervisor = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="subordinates")

    must_change_password = models.BooleanField(default=True, help_text="Detyron përdoruesin të ndryshojë fjalëkalimin në hyrjen e parë.")
    is_staff = models.BooleanField(default=False)  # Përdoret për qasje në Django Admin
    is_active = models.BooleanField(default=True)  # Mund të përdoret për të bllokuar llogarinë

    def __str__(self):
        dept_name = self.department.name if self.department else 'No Department'
        return f"{self.username} - {self.role} ({dept_name})"
