from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot, chat, update
from telegram import Update
from telegram.ext import CallbackContext, Filters, MessageHandler, Updater
from telegram.utils.request import Request

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
def handleMessage(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    reply_text = 'Test'
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

        updater.start_polling()
        update.idle()