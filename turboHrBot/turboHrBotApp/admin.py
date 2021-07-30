from django.contrib import admin
from .forms import AttendanceForm
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display=(
        'UserName', 
        'UserFullName', 
        'TimeStamp',
        'StartDate',
        'EndDate'
    )
    form = AttendanceForm