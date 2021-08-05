from django.db import models

class UserEventLog(models.Model):
    UserFullName = models.TextField(
        verbose_name='Telegram User Full Name'
    )
    TimeStamp = models.DateField(
        verbose_name='Date'
    )
    Event = models.TextField(
        verbose_name='User Event',
        max_length=150
    )

    def __str__(self):
        return f'{self.UserFullName}: {self.Event}'

    class Meta:
        verbose_name = 'User Event Log'

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
    WorkAmount = models.CharField(
        max_length=30,
        verbose_name='General Work Time',
        null=True
    )
    StartLocation = models.TextField(
        verbose_name='Start work location'
    )
    EndLocation = models.TextField(
        verbose_name='End work location',
        null=True
    )

    def GetDeltaTime(self):
        totalSeconds = (
            (
                self.EndDate.hour*3600
                +
                self.EndDate.minute*60
                +
                self.EndDate.second
            ) - (
                self.StartDate.hour*3600
                +
                self.StartDate.minute*60
                +
                self.StartDate.second
            )
        )
        hour, totalSeconds = divmod(totalSeconds, 3600)
        minute, totalSeconds = divmod(totalSeconds, 60)
        second = totalSeconds
        return "%02d:%02d:%02d" % (hour, minute, second)

    def __str__(self):
        if self.EndDate is None:
            return f'{self.UserFullName} Started at: {self.StartDate}'
        else:
            return f'{self.UserFullName} Worked today: {self.WorkAmount}'

    class Meta:
        verbose_name = 'Employee Attendance Information'
