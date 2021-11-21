import logging 
from flask import Flask, request
from telegram import Update, Bot, ReplyKeyboardMarkup, replymarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, Dispatcher
from utils import fetch_news, get_reply, topics_keyboard

# enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "2138742472:xxx"

# create Flask app object
app = Flask(__name__)
@app.route('/')
def index():
    return "Hello!"

# create view to handle webhooks
@app.route(f'/{TOKEN}', methods=['GET', 'POST'])
def webhook():
    """webhook view which receives updates from telegram"""
    # create update object from json-format request data
    update = Update.de_json(request.get_json(), bot)
    # process update
    dp.process_update(update)
    return "ok"


def start(update: Update, context: CallbackContext):
    print(update)
    author = update.message.from_user.first_name
    # msg = update.message.text
    reply = "Hi! {}".format(author)
    context.bot.send_message(chat_id = update.message.chat_id, text=reply)
     

def _help(update: Update, context: CallbackContext):
    help_txt = "Hey! This is a help text."
    context.bot.send_message(chat_id = update.message.chat_id, text=help_txt)


def reply_text(update: Update, context: CallbackContext):
    intent, reply = get_reply(update.message.text, update.message.chat_id)
    if intent == "get_news":
        reply_text = "Ok! I will show you news with {}".format(reply)
        context.bot.send_message(chat_id = update.message.chat_id, text=reply_text)
    else: 
        context.bot.send_message(chat_id = update.message.chat_id, text=reply)
    

def echo_sticker(update: Update, context: CallbackContext):
    context.bot.send_sticker(chat_id = update.message.chat_id, sticker=update.message.sticker.file_id)


def error(update, context):
    logger.error("Update '%s' caused error '%s'", update, context.error)


if __name__ == "__main__":
    # create telegram bot object
    bot = Bot(TOKEN)
    # set webhook for telegram bot 
    bot.set_webhook("https://02f5-122-161-50-67.ngrok.io/" + TOKEN)
    
    dp = Dispatcher(bot, None)
    # add handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", _help))
    # dp.add_handler(CommandHandler("news", news))
    dp.add_handler(MessageHandler(Filters.text, reply_text))
    dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
    dp.add_error_handler(error)
    app.run(port=8443)  