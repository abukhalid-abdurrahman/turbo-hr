from datetime import datetime
from django.http.response import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Attendance
import xlwt

def attendance(request):
    sqlRawQuery = 'SELECT * FROM turboHrBotApp_attendance'
    fullNameFilter = request.GET.get('name-filter')
    if fullNameFilter is not None:
        sqlRawQuery += f" WHERE UserFullName = '{fullNameFilter}'"
    usernameFilter = request.GET.get('username-filter')
    if usernameFilter is not None:
        if 'WHERE' in sqlRawQuery:
            sqlRawQuery += f" AND UserName = '{usernameFilter}'"
        else:
            sqlRawQuery += f" WHERE UserName = '{usernameFilter}'"

    dateFilter = request.GET.get('date-filter')
    if dateFilter is not None:
        if 'WHERE' in sqlRawQuery:
            sqlRawQuery += f" AND TimeStamp = date('{dateFilter}')"
        else:
            sqlRawQuery += f" WHERE TimeStamp = date('{dateFilter}')"

    attendances = Attendance.objects.raw(sqlRawQuery)
    print(attendances)
    paginatorInstance = Paginator(attendances, 5)
    pageNumber = request.GET.get('page', 1)
    attendances = paginatorInstance.get_page(pageNumber)
    return render(request, 'attendance.html', { 'data': attendances })

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
        'Start Location',
        'End Location' ]
    
    for columnIterator in range(len(columns)):
        workSheet.write(rowIterator, columnIterator, columns[columnIterator], fontStyle)

    fontStyle = xlwt.XFStyle()
    attendances = Attendance.objects.all().values_list(
        'id', 
        'UserName', 
        'UserFullName', 
        'TimeStamp', 
        'StartDate',
        'EndDate',
        'StartLocation',
        'EndLocation'
    )

    for item in attendances:
        rowIterator += 1
        for columnIterator in range(len(columns)):
            workSheet.write(rowIterator, columnIterator, str(item[columnIterator]), fontStyle)
    workBook.save(response)
    return response