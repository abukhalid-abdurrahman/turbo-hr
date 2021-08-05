# Generated by Django 3.2.4 on 2021-08-05 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UserId', models.IntegerField(verbose_name='Telegram User Identification Number')),
                ('UserName', models.TextField(verbose_name='Telegram User Name')),
                ('UserFullName', models.TextField(verbose_name='Telegram User Full Name')),
                ('TimeStamp', models.DateField(verbose_name='Date')),
                ('StartDate', models.TimeField(verbose_name='Start Time of Work')),
                ('EndDate', models.TimeField(null=True, verbose_name='End Time of Work')),
                ('WorkAmount', models.CharField(max_length=30, null=True, verbose_name='General Work Time')),
                ('StartLocation', models.TextField(verbose_name='Start work location')),
                ('EndLocation', models.TextField(null=True, verbose_name='End work location')),
            ],
            options={
                'verbose_name': 'Employee Attendance Information',
            },
        ),
        migrations.CreateModel(
            name='UserEventLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UserFullName', models.TextField(verbose_name='Telegram User Full Name')),
                ('TimeStamp', models.DateTimeField(verbose_name='Date')),
                ('Event', models.TextField(max_length=150, verbose_name='User Event')),
            ],
            options={
                'verbose_name': 'User Event Log',
            },
        ),
    ]
