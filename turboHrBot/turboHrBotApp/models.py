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

    def __str__(self):
        return f'{self.UserName} - {self.UserFullName}'

    class Meta:
        verbose_name = 'Employee Attendance Information'
     