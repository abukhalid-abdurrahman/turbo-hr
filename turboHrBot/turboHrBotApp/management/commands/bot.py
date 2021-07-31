from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot, chat, update
from telegram import Update
from telegram.ext import CallbackContext, Filters, MessageHandler, Updater
from telegram.ext.commandhandler import CommandHandler
from telegram.utils.request import Request
from datetime import date, datetime

from turboHrBotApp.models import Attendance

def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Exception Throwed: {e}'
            print(error_message)
            raise e
    return inner


@log_errors
def startHandler(update: Update, context: CallbackContext):
    userId = update.message.from_user.id
    userName = update.message.from_user.username
    userFullName = update.message.from_user.full_name
    today = date.today()
    timeStamp = today.strftime("%d/%m/%Y")
    startNow = datetime.now()

    if Attendance.objects.filter(UserId=userId, TimeStamp=timeStamp, EndDate__isnull=True, StartDate__isnull=False):
        reply_text = 'Thank You, but you already start your work today 🙂'
        update.message.reply_text(
            text=reply_text
        )
        return

    Attendance(
        UserId = userId,
        UserName = userName,
        UserFullName = userFullName,
        TimeStamp = timeStamp,
        StartDate = startNow.strftime("%d/%m/%Y %H:%M:%S")
    ).save()

    reply_text = 'Thank You! Have a productive day!'
    update.message.reply_text(
        text=reply_text
    )

@log_errors
def endHandler(update: Update, context: CallbackContext):
    userId = update.message.from_user.id
    today = date.today()
    timeStamp = today.strftime("%d/%m/%Y")
    endNow = datetime.now()

    if Attendance.objects.filter(UserId=userId, TimeStamp=timeStamp, EndDate__isnull=True, StartDate__isnull=False) is False:
        reply_text = 'Stop, but you didn\'t start your work today!'
        update.message.reply_text(
            text=reply_text
        )
        return

    if Attendance.objects.filter(UserId=userId, TimeStamp=timeStamp, EndDate__isnull=False, StartDate__isnull=False):
        reply_text = 'Thank you, but you have already warned me about the end of work!'
        update.message.reply_text(
            text=reply_text
        )
        return

    entityAttendance = Attendance.objects.get(UserId=userId, TimeStamp=timeStamp, EndDate__isnull=True, StartDate__isnull=False)
    entityAttendance.EndDate = endNow
    entityAttendance.save()

    deltaTime = entityAttendance.EndDate.hour - entityAttendance.StartDate.hour

    reply_text = f'Oh, you\'re done, have a good rest! Today You worked {deltaTime} hourse'
    update.message.reply_text(
        text=reply_text
    )

@log_errors
def handleMessage(update: Update, context: CallbackContext):
    reply_text = 'It seems that I did not understand you, you better tell me when you start or finish work 🙂'
    update.message.reply_text(
        text=reply_text
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
            token=settings.TOKEN,
            base_url=settings.PROXY_URL
        )

        updater = Updater(
            bot=bot,
            use_context=True
        )

        message_handler = MessageHandler(Filters.text, handleMessage)
        updater.dispatcher.add_handler(message_handler)

        startCommandHandler = CommandHandler('start', startHandler)
        updater.dispatcher.add_handler(startCommandHandler)

        endCommandHandler = CommandHandler('end', endHandler)
        updater.dispatcher.add_handler(endCommandHandler)

        updater.start_polling()
        update.idle()