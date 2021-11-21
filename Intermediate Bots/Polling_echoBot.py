import logging 
from telegram import Update, Bot, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from utils import fetch_news, get_reply, topics_keyboard

# enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "2138742472:xxx"


def start(update: Update, context: CallbackContext):
    print(update)
    author = update.message.from_user.first_name
    # msg = update.message.text
    reply = "Hi! {}".format(author)
    context.bot.send_message(chat_id = update.message.chat_id, text=reply)
     

def _help(update: Update, context: CallbackContext):
    help_txt = "Hey! This is a help text."
    context.bot.send_message(chat_id = update.message.chat_id, text=help_txt)


def news(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text="Choose a category", reply_markup=ReplyKeyboardMarkup(keyboard=topics_keyboard, one_time_keyboard=True))


def echo_text(update: Update, context: CallbackContext):
    reply = update.message.text
    context.bot.send_message(chat_id = update.message.chat_id, text=reply)
    

def echo_sticker(update: Update, context: CallbackContext):
    context.bot.send_sticker(chat_id = update.message.chat_id, sticker=update.message.sticker.file_id)


def error(update, context):
    logger.error("Update '%s' caused error '%s'", update, update.error)


def main():
    # create updater
    updater = Updater(TOKEN, use_context=True)
   
    # create dispatcher
    dp = updater.dispatcher
    
    # add handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", _help))
    dp.add_handler(CommandHandler("news", news))
    dp.add_handler(MessageHandler(Filters.text, echo_text))
    dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
    dp.add_error_handler(error)

    # start polling and wait for any signal to end the program
    updater.start_polling()
    logger.info("Started polling...")
    updater.idle()


if __name__ == "__main__":
    main()