from datetime import datetime
from django.http.response import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Attendance
import xlwt

def attendance(request):
    attendances = Attendance.objects.all()
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