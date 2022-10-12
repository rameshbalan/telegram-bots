from telegram.ext import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import telegram
import logging
import random

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def filename_generator(): 
    """ Creates a random string for the filename"""
    random_string = ''
    for _ in range(16):
        # Considering only upper and lowercase letters
        random_integer = random.randint(97, 97 + 26 - 1)
        flip_bit = random.randint(0, 1)
        # Convert to lowercase if the flip bit is on
        random_integer = random_integer - 32 if flip_bit == 1 else random_integer
        # Keep appending random characters using chr(x)
        random_string += (chr(random_integer))
    return random_string



def start_command(update, context):
    name = update.message.chat.first_name
    update.message.reply_text("இது ரமணியின் கோலத்திற்கான படங்களை ஏற்றுக்கொள்ளும் ஒரு போட் (Bot).")
    """Sends a message with three inline buttons attached."""
    keyboard = [

        [InlineKeyboardButton("நெழிவு கோலம்: 10 புள்ளிகளுக்கு கீழே", callback_data='NLT10')],
        [InlineKeyboardButton("நெழிவு கோலம்: 20 புள்ளிகளுக்கு கீழே", callback_data='NLT20')],
        [InlineKeyboardButton("நெழிவு கோலம்: 30 புள்ளிகளுக்கு கீழே", callback_data='NLT30')],
        [InlineKeyboardButton("கோலம்: 10 புள்ளிகளுக்கு கீழே", callback_data='LT10')],
        [InlineKeyboardButton("கோலம்: 20 புள்ளிகளுக்கு கீழே", callback_data='LT20')],
        [InlineKeyboardButton("கோலம்: 30 புள்ளிகளுக்கு கீழே", callback_data='LT30')],
        [InlineKeyboardButton("மார்கழி மாத கோலம்: 10 புள்ளிகளுக்கு கீழே", callback_data='MLT10')],
        [InlineKeyboardButton("மார்கழி மாத கோலம்: 20 புள்ளிகளுக்கு கீழே", callback_data='MLT20')],
        [InlineKeyboardButton("மார்கழி மாத கோலம்: 30 புள்ளிகளுக்கு கீழே", callback_data='MLT30')],

    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('கீழே காட்டப்பட்டுள்ள விருப்பங்களிலிருந்து, கோலத்தின் வகையைத் தேர்ந்தெடுக்கவும்', reply_markup=reply_markup)

def image_handler(update, context):
    file = update.message.photo[-1].file_id
    obj = context.bot.get_file(file)
    obj.download(custom_path = kolamCategory)
    
    update.message.reply_text("உங்கள் படத்தை பதிவேற்றியதற்கு நன்றி!")

def button(update, context) -> None:
    global kolamCategory
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    fname = filename_generator()
    kolamCategory = "ramanikolam.github.io/img/"+query.data+"/"+fname+".jpg"
    query.edit_message_text(text=f"உங்கள் கோலத்தை இப்போது பதிவேற்றவும்.")

def main():
    TOKEN = "5242328866:AAGaLIJmZNSJmaixWUOMZ8kQr8gjTocH83A"
    updater = Updater(TOKEN, use_context = True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.photo, image_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()