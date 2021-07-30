from django.contrib import admin
from turboHrBotApp.models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display=(
        'UserName', 
        'UserFullName', 
        'TimeStamp',
        'StartDate',
        'EndDate'
    )