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
    pass

@log_errors
def endHandler(update: Update, context: CallbackContext):
    pass

@log_errors
def handleMessage(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    today = date.today()
    timeStamp = today.strftime("%d/%m/%Y")
    startNow = datetime.now()
    
    entity, _ = Attendance.objects.get_or_create(
        UserId = update.message.from_user.id,
        defaults= {
            'UserId': update.message.from_user.id,
            'UserName': update.message.from_user.username,
            'UserFullName': update.message.from_user.full_name,
            'TimeStamp': timeStamp,
            'StartDate': startNow.strftime("%d/%m/%Y %H:%M:%S")
        }
    )

    Attendance.objects.get_or_create(
        UserId = update.message.from_user.id,
        UserName = update.message.from_user.username,
        UserFullName = update.message.from_user.full_name,
        TimeStamp = timeStamp,
        StartDate = startNow.strftime("%d/%m/%Y %H:%M:%S")
    ).save()

    reply_text = 'Thank You! Have A Good Day!'
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