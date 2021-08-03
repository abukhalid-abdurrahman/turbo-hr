from django.contrib import admin
from .forms import AttendanceForm, UserEventLogForm
from .models import Attendance, UserEventLog

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

@admin.register(UserEventLog)
class UserEventLogAdmin(admin.ModelAdmin):
    list_display=(
        'UserFullName', 
        'TimeStamp',
        'Event'
    )
    form = UserEventLogForm