from datetime import timedelta
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
    TimeStamp = models.DateField(
        verbose_name='Date'
    )
    StartDate = models.TimeField(
        verbose_name='Start Time of Work'
    )
    EndDate = models.TimeField(
        verbose_name='End Time of Work',
        null=True
    )
    StartLocation = models.TextField(
        verbose_name='Start work location'
    )
    EndLocation = models.TextField(
        verbose_name='End work location',
        null=True
    )

    def __str__(self):
        if self.EndDate is None:
            return f'{self.UserFullName} Started at: {self.StartDate}'
        else:
            deltaTime = self.EndDate.second - self.StartDate.second
            return f'{self.UserFullName} Worked today: {timedelta(seconds=deltaTime)}'

    class Meta:
        verbose_name = 'Employee Attendance Information'
     