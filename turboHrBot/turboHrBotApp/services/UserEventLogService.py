import csv
from datetime import datetime
from django.core.paginator import Paginator
from django.http.response import HttpResponse
import xlwt
from turboHrBotApp.models import UserEventLog


class UserEventLogService():

    def GetUserEventLogs(self, page, name, date):
        sqlRawQuery = 'SELECT * FROM turboHrBotApp_usereventLog'

        if name is not None and name is not '':
            sqlRawQuery += f" WHERE UserFullName = '{name}'"
        if date is not None and date is not '':
            if 'WHERE' in sqlRawQuery:
                sqlRawQuery += f" AND TimeStamp = date('{date}')"
            else:
                sqlRawQuery += f" WHERE TimeStamp = date('{date}')"

        logs = UserEventLog.objects.raw(sqlRawQuery)
        paginatorInstance = Paginator(logs, 5)
        pageNumber = page
        logs = paginatorInstance.get_page(pageNumber)
        return logs

    def ExportUserEventLogsExcel(self, name, date):
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
        if name is not None and name is not '':
            sqlRawQuery += f" WHERE UserFullName = '{name}'"
        if date is not None and date is not '':
            if 'WHERE' in sqlRawQuery:
                sqlRawQuery += f" AND TimeStamp = date('{date}')"
            else:
                sqlRawQuery += f" WHERE TimeStamp = date('{date}')"

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

    def ExportUserEventLogsCsv(self, name, date):
        response=HttpResponse(content_type='application/text/csv')
        response['Content-Disposition'] = f'attachment; filename=User Event Log-{str(datetime.now())}.csv'

        writer = csv.writer(response)
        writer.writerow(['Log Id', 'User Full Name', 'Date', 'Event'])

        sqlRawQuery = 'SELECT * FROM turboHrBotApp_usereventLog'
        if name is not None and name is not '':
            sqlRawQuery += f" WHERE UserFullName = '{name}'"
        if date is not None and date is not '':
            if 'WHERE' in sqlRawQuery:
                sqlRawQuery += f" AND TimeStamp = date('{date}')"
            else:
                sqlRawQuery += f" WHERE TimeStamp = date('{date}')"

        logs = UserEventLog.objects.raw(sqlRawQuery)

        for log in logs:
            writer.writerow([str(log.id), str(log.UserFullName), str(log.TimeStamp), str(log.Event)])
        return response