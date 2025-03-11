from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee, Department, Position

class EmployeeAdmin(UserAdmin):
    model = Employee

    list_display = ('username', 'email', 'role', 'department', 'position', 'get_supervisor', 'is_active', 'is_staff')
    list_filter = ('role', 'department', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'role', 'position', 'supervisor__username')

    ordering = ('username',)

    fieldsets = (
        ("🔹 Informacioni Kryesor", {
            "fields": ("username", "password", "first_name", "last_name", "email", "date_joined")
        }),
        ("📌 Departamenti & Pozicioni", {
            "fields": ("role", "department", "position")
        }),
        ("👤 Mbikëqyrësi", {
            "fields": ("supervisor",)
        }),
        ("🔒 Siguria & Statusi", {
            "fields": ("must_change_password", "is_active", "is_staff", "is_superuser")
        }),
        ("⚙️ Lejet & Grupet", {
            "fields": ("groups", "user_permissions")
        }),
    )

    # ✅ Përmirësimi i krijimit të përdoruesve të rinj
    add_fieldsets = (
        ("➕ Shto Përdorues të Ri", {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "role", "department", "position", "supervisor", "must_change_password", "is_active", "is_staff"),
        }),
    )

    def get_supervisor(self, obj):
        return obj.supervisor.username if obj.supervisor else "Nuk ka mbikëqyrës"

    get_supervisor.short_description = "Mbikëqyrësi"

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department)
admin.site.register(Position)  
