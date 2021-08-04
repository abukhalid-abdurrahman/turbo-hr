from django.shortcuts import render
from services import UserEventLogService, AttendanceService
userEventLogService = UserEventLogService()
attendanceService = AttendanceService()

def attendance(request):
    fullNameFilter = request.GET.get('name-filter')
    usernameFilter = request.GET.get('username-filter')
    dateFilter = request.GET.get('date-filter')
    page = request.GET.get('page', 1)
    attendances = attendanceService.GetAttendances(page, fullNameFilter, usernameFilter, dateFilter)
    return render(request, 'attendance.html', { 
        'data': attendances, 
        'usernameFilter': '' if usernameFilter is None else usernameFilter,
        'fullNameFilter': '' if fullNameFilter is None else fullNameFilter,
        'dateFilter': '' if dateFilter is None else dateFilter
    })

def exportExcel(request):
    return attendanceService.ExportAttendanceExcel(request)

def exportAttendanceCsv(request):
    return attendanceService.ExportAttendanceCsv(request)

def logs(request):
    fullNameFilter = request.GET.get('name-filter')
    dateFilter = request.GET.get('date-filter')
    page = request.GET.get('page', 1)
    logs = userEventLogService.GetUserEventLogs(page, fullNameFilter, dateFilter)
    return render(request, 'logs.html', { 
        'data': logs,
        'fullNameFilter': '' if fullNameFilter is None else fullNameFilter,
        'dateFilter': '' if dateFilter is None else dateFilter
    }) 

def exportLogsExcel(request):
    dateFilter = request.GET.get('date-filter')
    fullNameFilter = request.GET.get('name-filter')
    response = UserEventLogService.ExportUserEventLogsExcel(fullNameFilter, dateFilter)
    return response

def exportLogsCsv(request):
    fullNameFilter = request.GET.get('name-filter')
    dateFilter = request.GET.get('date-filter')
    response = userEventLogService.ExportUserEventLogsCsv(fullNameFilter, dateFilter)
    return response