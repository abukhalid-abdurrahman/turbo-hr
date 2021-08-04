from django.urls import path
from . import views 

urlpatterns = [
    path('', views.attendance),
    path('attendance', views.attendance),
    path('exportExcel', views.exportExcel),
    path('exportLogsExcel', views.exportLogsExcel),
    path('exportLogsCsv', views.exportLogsCsv),
    path('exportLogsPdf', views.exportLogsPdf),
    path('exportAttendanceCsv', views.exportAttendanceCsv),
    path('exportAttendancePdf', views.exportAttendancePdf)
]
