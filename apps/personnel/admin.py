from django.contrib import admin
from .models import Employee, Department

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'first_name', 'last_name', 'department', 'hire_date')
    search_fields = ('employee_id', 'last_name')
    list_filter = ('department',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
