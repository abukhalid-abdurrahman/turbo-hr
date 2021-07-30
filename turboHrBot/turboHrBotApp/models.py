from django.db import models

class Attendance(models.Model):
    UserId = models.IntegerField(
        verbose_name='Telegram User Identification Number'
    )
    UserName = models.TextField(
        verbose_name='Telegram User Name'
    )
    UserFullName = models.TextField(
        verbose_name='Telegram User Full Name'
    )
    TimeStamp = models.DateTimeField(
        verbose_name='Date'
    )
    StartDate = models.DateTimeField(
        verbose_name='Start Time of Work'
    )
    EndDate = models.DateTimeField(
        verbose_name='End Time of Work'
    )
     