from django import forms
from django.forms import fields
from .models import Attendance

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
            'StartLocation',
            'EndLocation'
        )
        widgets = {
            'UserName': forms.TextInput,
            'UserFullName': forms.TextInput,
            'StartLocation': forms.TextInput,
            'EndLocation': forms.TextInput
        }