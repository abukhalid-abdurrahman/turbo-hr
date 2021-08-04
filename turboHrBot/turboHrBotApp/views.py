from datetime import datetime
from django.http.response import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Attendance, UserEventLog
import xlwt
import csv

def logs(request):
    sqlRawQuery = 'SELECT * FROM turboHrBotApp_usereventLog'
    fullNameFilter = request.GET.get('name-filter')
    if fullNameFilter is not None and fullNameFilter is not '':
        sqlRawQuery += f" WHERE UserFullName = '{fullNameFilter}'"
    dateFilter = request.GET.get('date-filter')
    if dateFilter is not None and dateFilter is not '':
        if 'WHERE' in sqlRawQuery:
            sqlRawQuery += f" AND TimeStamp = date('{dateFilter}')"
        else:
            sqlRawQuery += f" WHERE TimeStamp = date('{dateFilter}')"

    logs = UserEventLog.objects.raw(sqlRawQuery)
    paginatorInstance = Paginator(logs, 5)
    pageNumber = request.GET.get('page', 1)
    logs = paginatorInstance.get_page(pageNumber)

    return render(request, 'logs.html', { 
        'data': logs,
        'fullNameFilter': '' if fullNameFilter is None else fullNameFilter,
        'dateFilter': '' if dateFilter is None else dateFilter
    }) 

def attendance(request):
    sqlRawQuery = 'SELECT * FROM turboHrBotApp_attendance'
    fullNameFilter = request.GET.get('name-filter')
    if fullNameFilter is not None and fullNameFilter is not '':
        sqlRawQuery += f" WHERE UserFullName = '{fullNameFilter}'"
    usernameFilter = request.GET.get('username-filter')
    if usernameFilter is not None and usernameFilter is not '':
        if 'WHERE' in sqlRawQuery:
            sqlRawQuery += f" AND UserName = '{usernameFilter}'"
        else:
            sqlRawQuery += f" WHERE UserName = '{usernameFilter}'"

    dateFilter = request.GET.get('date-filter')
    if dateFilter is not None and dateFilter is not '':
        if 'WHERE' in sqlRawQuery:
            sqlRawQuery += f" AND TimeStamp = date('{dateFilter}')"
        else:
            sqlRawQuery += f" WHERE TimeStamp = date('{dateFilter}')"

    attendances = Attendance.objects.raw(sqlRawQuery)
    paginatorInstance = Paginator(attendances, 5)
    pageNumber = request.GET.get('page', 1)
    attendances = paginatorInstance.get_page(pageNumber)
    return render(request, 'attendance.html', { 
        'data': attendances, 
        'usernameFilter': '' if usernameFilter is None else usernameFilter,
        'fullNameFilter': '' if fullNameFilter is None else fullNameFilter,
        'dateFilter': '' if dateFilter is None else dateFilter
    })


def exportLogsExcel(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename=User Event Log-{str(datetime.now())}.xls'

    workBook = xlwt.Workbook(encoding='utf-8')
    workSheet = workBook.add_sheet('User Event Log')
    rowIterator = 0
    fontStyle = xlwt.XFStyle()
    fontStyle.font.bold = True

    columns = [
        'Log Id',
        'Full Name', 
        'Date', 
        'Event' ]
    
    for columnIterator in range(len(columns)):
        workSheet.write(rowIterator, columnIterator, columns[columnIterator], fontStyle)

    fontStyle = xlwt.XFStyle()

    sqlRawQuery = 'SELECT * FROM turboHrBotApp_usereventLog'
    fullNameFilter = request.GET.get('name-filter')
    if fullNameFilter is not None and fullNameFilter is not '':
        sqlRawQuery += f" WHERE UserFullName = '{fullNameFilter}'"
    dateFilter = request.GET.get('date-filter')
    if dateFilter is not None and dateFilter is not '':
        if 'WHERE' in sqlRawQuery:
            sqlRawQuery += f" AND TimeStamp = date('{dateFilter}')"
        else:
            sqlRawQuery += f" WHERE TimeStamp = date('{dateFilter}')"

    logs = UserEventLog.objects.raw(sqlRawQuery)

    for item in logs:
        rowIterator += 1
        columnIterator = 0
        workSheet.write(rowIterator, columnIterator, str(item.id), fontStyle)
        workSheet.write(rowIterator, columnIterator + 1, str(item.UserFullName), fontStyle)
        workSheet.write(rowIterator, columnIterator + 2, str(item.TimeStamp), fontStyle)
        workSheet.write(rowIterator, columnIterator + 3, str(item.Event), fontStyle)
    workBook.save(response)
    return response


def exportExcel(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename=Attendance-{str(datetime.now())}.xls'

    workBook = xlwt.Workbook(encoding='utf-8')
    workSheet = workBook.add_sheet('Attendance')
    rowIterator = 0
    fontStyle = xlwt.XFStyle()
    fontStyle.font.bold = True

    columns = [
        'Id', 
        'User Name', 
        'Full Name', 
        'Date', 
        'Start Time',
        'End Time',
        'Work Amount',
        'Start Location',
        'End Location' ]
    
    for columnIterator in range(len(columns)):
        workSheet.write(rowIterator, columnIterator, columns[columnIterator], fontStyle)

    fontStyle = xlwt.XFStyle()

    sqlRawQuery = 'SELECT * FROM turboHrBotApp_attendance'
    fullNameFilter = request.GET.get('name-filter')
    if fullNameFilter is not None and fullNameFilter is not '':
        sqlRawQuery += f" WHERE UserFullName = '{fullNameFilter}'"
    usernameFilter = request.GET.get('username-filter')
    if usernameFilter is not None and usernameFilter is not '':
        if 'WHERE' in sqlRawQuery:
            sqlRawQuery += f" AND UserName = '{usernameFilter}'"
        else:
            sqlRawQuery += f" WHERE UserName = '{usernameFilter}'"

    dateFilter = request.GET.get('date-filter')
    if dateFilter is not None and dateFilter is not '':
        if 'WHERE' in sqlRawQuery:
            sqlRawQuery += f" AND TimeStamp = date('{dateFilter}')"
        else:
            sqlRawQuery += f" WHERE TimeStamp = date('{dateFilter}')"

    attendances = Attendance.objects.raw(sqlRawQuery)

    for item in attendances:
        rowIterator += 1
        columnIterator = 0
        workSheet.write(rowIterator, columnIterator, str(item.id), fontStyle)
        workSheet.write(rowIterator, columnIterator + 1, str(item.UserName), fontStyle)
        workSheet.write(rowIterator, columnIterator + 2, str(item.UserFullName), fontStyle)
        workSheet.write(rowIterator, columnIterator + 3, str(item.TimeStamp), fontStyle)
        workSheet.write(rowIterator, columnIterator + 4, str(item.StartDate), fontStyle)
        workSheet.write(rowIterator, columnIterator + 5, str(item.EndDate), fontStyle)
        workSheet.write(rowIterator, columnIterator + 6, str(item.WorkAmount), fontStyle)
        workSheet.write(rowIterator, columnIterator + 7, str(item.StartLocation), fontStyle)
        workSheet.write(rowIterator, columnIterator + 8, str(item.EndLocation), fontStyle)
    workBook.save(response)
    return response

def exportLogsCsv(request):
    response=HttpResponse(content_type='application/text/csv')
    response['Content-Disposition'] = f'attachment; filename=User Event Log-{str(datetime.now())}.csv'

    writer = csv.writer(response)
    writer.writerow(['Log Id', 'User Full Name', 'Date', 'Event'])

    sqlRawQuery = 'SELECT * FROM turboHrBotApp_usereventLog'
    fullNameFilter = request.GET.get('name-filter')
    if fullNameFilter is not None and fullNameFilter is not '':
        sqlRawQuery += f" WHERE UserFullName = '{fullNameFilter}'"
    dateFilter = request.GET.get('date-filter')
    if dateFilter is not None and dateFilter is not '':
        if 'WHERE' in sqlRawQuery:
            sqlRawQuery += f" AND TimeStamp = date('{dateFilter}')"
        else:
            sqlRawQuery += f" WHERE TimeStamp = date('{dateFilter}')"

    logs = UserEventLog.objects.raw(sqlRawQuery)

    for log in logs:
        writer.writerow([str(log.id), str(log.UserFullName), str(log.TimeStamp), str(log.Event)])
    return response

def exportAttendanceCsv(request):
    response=HttpResponse(content_type='application/text/csv')
    response['Content-Disposition'] = f'attachment; filename=User Event Log-{str(datetime.now())}.csv'

    writer = csv.writer(response)

    columns = [
        'Id', 
        'User Name', 
        'Full Name', 
        'Date', 
        'Start Time',
        'End Time',
        'Work Amount',
        'Start Location',
        'End Location' ]
    writer.writerow(columns)

    sqlRawQuery = 'SELECT * FROM turboHrBotApp_attendance'
    fullNameFilter = request.GET.get('name-filter')
    if fullNameFilter is not None and fullNameFilter is not '':
        sqlRawQuery += f" WHERE UserFullName = '{fullNameFilter}'"
    usernameFilter = request.GET.get('username-filter')
    if usernameFilter is not None and usernameFilter is not '':
        if 'WHERE' in sqlRawQuery:
            sqlRawQuery += f" AND UserName = '{usernameFilter}'"
        else:
            sqlRawQuery += f" WHERE UserName = '{usernameFilter}'"

    dateFilter = request.GET.get('date-filter')
    if dateFilter is not None and dateFilter is not '':
        if 'WHERE' in sqlRawQuery:
            sqlRawQuery += f" AND TimeStamp = date('{dateFilter}')"
        else:
            sqlRawQuery += f" WHERE TimeStamp = date('{dateFilter}')"

    attendances = Attendance.objects.raw(sqlRawQuery)
    for attendance in attendances:
        writer.writerow([attendance.UserId, attendance.UserName, attendance.UserFullName, 
            attendance.TimeStamp, attendance.StartDate, 
            attendance.EndDate, attendance.WorkAmount, 
            attendance.StartLocation, attendance.EndLocation])
    return response