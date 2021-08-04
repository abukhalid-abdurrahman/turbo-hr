import csv
import xlwt
from datetime import datetime
from django.core.paginator import Paginator
from turboHrBotApp.models import Attendance
from django.http.response import HttpResponse


class AttendanceService():

    def GetAttendances(self, page, name, username, date):
        sqlRawQuery = 'SELECT * FROM turboHrBotApp_attendance'
        
        if name is not None and name is not '':
            sqlRawQuery += f" WHERE UserFullName = '{name}'"
        if username is not None and username is not '':
            if 'WHERE' in sqlRawQuery:
                sqlRawQuery += f" AND UserName = '{username}'"
            else:
                sqlRawQuery += f" WHERE UserName = '{username}'"
        if date is not None and date is not '':
            if 'WHERE' in sqlRawQuery:
                sqlRawQuery += f" AND TimeStamp = date('{date}')"
            else:
                sqlRawQuery += f" WHERE TimeStamp = date('{date}')"

        attendances = Attendance.objects.raw(sqlRawQuery)
        paginatorInstance = Paginator(attendances, 5)
        pageNumber = page
        attendances = paginatorInstance.get_page(pageNumber)
        return attendances

    def ExportAttendanceExcel(self, request):
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

    def ExportAttendanceCsv(self, request):
        response=HttpResponse(content_type='application/text/csv')
        response['Content-Disposition'] = f'attachment; filename=Attendance-{str(datetime.now())}.csv'

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