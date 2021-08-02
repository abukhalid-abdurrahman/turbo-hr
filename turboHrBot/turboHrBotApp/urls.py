from django.urls import path
from . import views 

urlpatterns = [
    path('', views.attendance),
    path('attendance', views.attendance),
    path('exportExcel', views.exportExcel)
]
