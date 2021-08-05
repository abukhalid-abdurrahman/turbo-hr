from django import forms
from .models import Attendance, UserEventLog

class UserEventLogForm(forms.ModelForm):
    class Meta:
        model = UserEventLog
        fields = (
            'UserFullName', 
            'TimeStamp',
            'Event'
        )
        widgets = {
            'UserFullName': forms.TextInput, 
            'Event': forms.TextInput
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = (
            'UserId',
            'UserName', 
            'UserFullName', 
            'TimeStamp',
            'StartDate',
            'EndDate',
            'WorkAmount',
            'StartLocation',
            'EndLocation'
        )
        widgets = {
            'UserName': forms.TextInput,
            'UserFullName': forms.TextInput,
            'StartLocation': forms.TextInput,
            'EndLocation': forms.TextInput
        }