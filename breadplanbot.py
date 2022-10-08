# Import Libraries
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from random import randint
import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Secret ID for the bot: API
updater = Updater("<API>",
                  use_context=True)

# Commands
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "ஹே ரோபோ.. யோ ரோபோ..ஹே இன்பா நன்பா come-on lets go. \
        Boom Boom Robo-Da Robo-Da Robo-Da \
        Zoom Zoom Robo-Da Robo-Da Robo-Da\
        நான் ஒரு உணவு திட்டமிடும் ரோபோ! \
        அடுத்த வாரத்திற்கான உணவுத் திட்டத்தை உருவாக்க, /gimmemyplan ஐ அனுப்பவும்")

def help(update: Update, context: CallbackContext):
    update.message.reply_text("அடுத்த வாரத்திற்கான உணவுத் திட்டத்தை உருவாக்க - /gimmemyplan")

def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "மன்னிக்கவும் '%s' சரியான கட்டளை அல்ல" % update.message.text)

def gimmemyplan(update: Update, context: CallbackContext):
    generate_plan()
    chat_id = update.message.chat_id
    context.bot.sendMessage(chat_id, "நான் தற்போது ஒரு சுவையான வாரத்திற்கான அட்டவணையை தயார் செய்து வருகிறேன், தயவு செய்து காத்திருங்கள்...")
    context.bot.sendDocument(chat_id = chat_id,\
                             caption = 'அடுத்த வாரத்திற்கான உணவுத் திட்டம் தயார். உண்டு மகிழுங்கள்.',\
                             document = open("mealplan.pdf", "rb"))

def glue(x,y):
    value = " | ".join([str(x),str(y)])
    return value

def generate_plan():

    bft_opts = ["Oats with Blueberries and Strawberries",\
    "Broccoli & Carrots | Scrambled Eggs | Potato Patty",\
    "Cheerios | Boiled Eggs",\
    "Bread and Jam/Hummus | Scrambled Eggs | Guacamole",\
    "Oats with Blueberries and Strawberries"]
    lun_opts = ["Rice","Variety Rice"]
    kulambu_opts = ["Rasam Paruppu",\
    "Okra Sambar", \
    "Karuppu Sundal Kulambu",\
    "Dal Palak",\
    "Ennai Kathrikai Kulambu",
    "Pachapayaru Kulambu"]
    side_opts = ["Keerai Poriyal",\
    "Cabbage Poriyal",\
    "Cauliflower Poriyal",\
    "Carrot Poriyal",\
    "Potato Poriyal",\
    "Green Beans Poriyal",\
    "Beetroot Poriyal"]
    gravy_opts = ["Potato Peas Gravy",\
    "Paneer Gravy",\
    "Mushroom Gravy",\
    "Vegetable Kurma",\
    "Channa Masala"]
    chutney_opts = ["Tomato Chuntney",\
    "Mint Chuntney",\
    "Cilantro Chuntney",\
    "Peanut Chuntney",\
    "Coconut Chuntney",\
    "Kadalai Paruppu Chuntney",\
    "Kaara Chuntney"]
    din_opts = ["Chappathi","Poha","Dosa","Idli"]

    breakfast = [\
                 bft_opts[randint(0,len(bft_opts)-1)],\
                 bft_opts[randint(0,len(bft_opts)-1)],\
                 bft_opts[randint(0,len(bft_opts)-1)],\
                 bft_opts[randint(0,len(bft_opts)-1)],\
                 bft_opts[randint(0,len(bft_opts)-1)]]
    lunch = [\
                 glue(lun_opts[0],\
                    glue(kulambu_opts[randint(0,len(kulambu_opts)-1)],side_opts[randint(0,len(side_opts)-1)])),\
                 glue(lun_opts[1],side_opts[randint(0,len(side_opts)-1)]),\
                 glue(lun_opts[0],\
                    glue(kulambu_opts[randint(0,len(kulambu_opts)-1)],side_opts[randint(0,len(side_opts)-1)])),\
                 glue(lun_opts[0],\
                    glue(kulambu_opts[randint(0,len(kulambu_opts)-1)],side_opts[randint(0,len(side_opts)-1)])),\
                 glue(lun_opts[0],\
                    glue("Omelet",kulambu_opts[randint(0,len(kulambu_opts)-1)])),\
                 ]
    dinner = [\
                 glue(din_opts[0],gravy_opts[randint(0,len(gravy_opts)-1)]),\
                 glue(din_opts[1],chutney_opts[randint(0,len(chutney_opts)-1)]),\
                 glue(din_opts[2],chutney_opts[randint(0,len(chutney_opts)-1)]),\
                 glue(din_opts[2],chutney_opts[randint(0,len(chutney_opts)-1)]),\
                 glue(din_opts[3],chutney_opts[randint(0,len(chutney_opts)-1)]),\
                 ]

    m = [breakfast,lunch,dinner]
    df = pd.DataFrame(np.asarray(m), columns = ["M","T","W","Th","Fr"])
    #https://stackoverflow.com/questions/32137396/how-do-i-plot-only-a-table-in-matplotlib
    fig, ax =plt.subplots(figsize=(5,7))
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=df.values,colLabels=df.columns,loc='center')
    the_table.set_fontsize(32)
    the_table.scale(10, 10)

    #https://stackoverflow.com/questions/4042192/reduce-left-and-right-margins-in-matplotlib-plot
    pp = PdfPages("mealplan.pdf")
    pp.savefig(fig, bbox_inches='tight')
    pp.close()

# Declare the commands to the bot
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('gimmemyplan', gimmemyplan))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))

# Start the bot
updater.start_polling()
