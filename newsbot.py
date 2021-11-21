import logging, traceback, html, json
from flask import Flask, request
from telegram import Update, Bot, ReplyKeyboardMarkup, ParseMode, replymarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, Dispatcher
from utils import fetch_news, get_reply, topics_keyboard

# enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "2138742472:xxx"

DEVELOPER_CHAT_ID = 902424541

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


def news(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text="Choose a category", reply_markup=ReplyKeyboardMarkup(keyboard=topics_keyboard, one_time_keyboard=True))


def reply_text(update: Update, context: CallbackContext):
    intent, reply = get_reply(update.message.text, update.message.chat_id)
    if intent == "get_news":
        # reply_text = "Ok! I will show you news with {}".format(reply)
        articles = fetch_news(reply)
        for article in articles:
            context.bot.send_message(chat_id = update.message.chat_id, text=article['link'])
    else: 
        context.bot.send_message(chat_id = update.message.chat_id, text=reply)
    

def echo_sticker(update: Update, context: CallbackContext):
    context.bot.send_sticker(chat_id = update.message.chat_id, sticker=update.message.sticker.file_id)

   
def error_handler(update: object, context: CallbackContext) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    
    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f'An exception was raised while handling an update\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )
    # Finally, send the message
    context.bot.send_message(chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML)


# create telegram bot object
bot = Bot(TOKEN)
# set webhook for telegram bot 
try:
    bot.set_webhook("https://get-informed-newsbot.herokuapp.com/" + TOKEN)
except Exception as e:
    print(e)

dp = Dispatcher(bot, None)
# add handlers
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", _help))
dp.add_handler(CommandHandler("news", news))
dp.add_handler(MessageHandler(Filters.text, reply_text))
dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
dp.add_error_handler(error_handler)


if __name__ == "__main__":
    app.run(port=8443)  