from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot, ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext, Filters, MessageHandler, Updater
from telegram.ext.commandhandler import CommandHandler
from telegram.utils.request import Request
from datetime import date, datetime

from turboHrBotApp.models import Attendance, UserEventLog

def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Exception Throwed: {e}'
            print(error_message)
            raise e
    return inner


def GetReplyKeyboard():
    buttons = [['Check In', 'Check Out']]
    return ReplyKeyboardMarkup(buttons, one_time_keyboard=False)

def CheckIn(payload):
    userId = payload.message.from_user.id
    location = payload.message.chat.location
    userName = payload.message.from_user.username
    userFullName = payload.message.from_user.full_name
    timeStamp = date.today()

    UserEventLog(
        UserFullName=userFullName,
        TimeStamp=timeStamp,
        Event='Announced the start of work'
    ).save()

    if Attendance.objects.filter(UserId=userId, TimeStamp=timeStamp, EndDate__isnull=True, StartDate__isnull=False):
        reply_text = 'Thank You, but you already start your work today 🙂'
        payload.message.reply_text(
            text=reply_text,
            reply_markup=GetReplyKeyboard()
        )
        return

    if Attendance.objects.filter(UserId=userId, TimeStamp=timeStamp, EndDate__isnull=False, StartDate__isnull=False):
        reply_text = 'You seem to have done enough work today, take a break!'
        payload.message.reply_text(
            text=reply_text,
            reply_markup=GetReplyKeyboard()
        )
        return

    address = 'Not Pointed!'
    if location is not None:
        address = location.address

    Attendance(
        UserId = userId,
        UserName = userName,
        UserFullName = userFullName,
        TimeStamp = timeStamp,
        StartDate = datetime.now(),
        StartLocation = address
    ).save()

    reply_text = 'Thank You! Have a productive day!'
    payload.message.reply_text(
        text=reply_text,
        reply_markup=GetReplyKeyboard()
    )

def CheckOut(payload):
    userFullName = payload.message.from_user.full_name
    userId = payload.message.from_user.id
    location = payload.message.chat.location
    timeStamp = date.today()

    UserEventLog(
        UserFullName=userFullName,
        TimeStamp=timeStamp,
        Event='Announced the end of work'
    ).save()

    if not (Attendance.objects.filter(UserId=userId, TimeStamp=timeStamp)):
        reply_text = 'Stop, but you didn\'t start your work today!'
        payload.message.reply_text(
            text=reply_text,
            reply_markup=GetReplyKeyboard()
        )
        return

    if Attendance.objects.filter(UserId=userId, TimeStamp=timeStamp, EndDate__isnull=False, StartDate__isnull=False):
        reply_text = 'Thank you, but you have already warned me about the end of work!'
        payload.message.reply_text(
            text=reply_text,
            reply_markup=GetReplyKeyboard()
        )
        return

    entityAttendance = Attendance.objects.get(UserId=userId, TimeStamp=timeStamp, EndDate__isnull=True, StartDate__isnull=False)
    if entityAttendance is None:
        reply_text = 'Ooops! Somethin goes wrong!'
        payload.message.reply_text(
            text=reply_text,
            reply_markup=GetReplyKeyboard()
        )
        return

    address = 'Not Pointed!'
    if location is not None:
        address = location.address

    entityAttendance.EndDate = datetime.now()
    entityAttendance.WorkAmount = entityAttendance.GetDeltaTime()
    entityAttendance.EndLocation = address
    entityAttendance.save()

    reply_text = f'Oh, you\'re done, have a good rest! Today You worked {entityAttendance.WorkAmount}!'
    payload.message.reply_text(
        text=reply_text,
        reply_markup=GetReplyKeyboard()
    )


@log_errors
def startHandler(update: Update, context: CallbackContext):
    CheckIn(update)

@log_errors
def endHandler(update: Update, context: CallbackContext):
    CheckOut(update)

@log_errors
def handleMessage(update: Update, context: CallbackContext):
    userFullName = update.message.from_user.full_name
    messageText = update.message.text

    if messageText == 'Check In':
        CheckIn(update)
        return
    elif messageText == 'Check Out':
        CheckOut(update)
        return

    if len(messageText) > 100:
        messageText = messageText[:100]

    UserEventLog(
        UserFullName=userFullName,
        TimeStamp=date.today(),
        Event=f'Write Message: {messageText}'
    ).save()

    reply_text = 'It seems that I did not understand you, you better tell me when you start or finish work 🙂'
    update.message.reply_text(
        text=reply_text,
        reply_markup=GetReplyKeyboard()
    )

class Command(BaseCommand):
    help = 'Telegram HR Bot'

    def handle(self, *args, **options):
        req = Request (
            connect_timeout=0.5,
            read_timeout=1.0
        )
        bot = Bot(
            request=req,
            token=settings.TOKEN
        )

        updater = Updater(
            bot=bot,
            use_context=True
        )

        startCommandHandler = CommandHandler('start', startHandler)
        updater.dispatcher.add_handler(startCommandHandler)

        endCommandHandler = CommandHandler('end', endHandler)
        updater.dispatcher.add_handler(endCommandHandler)

        message_handler = MessageHandler(Filters.text, handleMessage)
        updater.dispatcher.add_handler(message_handler)

        updater.start_polling()