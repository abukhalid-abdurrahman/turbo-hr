from django.shortcuts import render
from .models import Attendance

def attendance(request):
    attendances = Attendance.objects.all()
    return render(request, 'attendance.html', { 'data': attendances })