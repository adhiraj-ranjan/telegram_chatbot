import telegram.ext
from util import get_response

with open("token.txt", "r") as f:
    token = f.read().strip()

def start(update, context):
    update.message.reply_text("Hi, my name is Eliza. What is weighing on your mind?")

def reply(update, context):
    response = get_response(update.message.text, f"data/{update.message.chat.id}")
    if response:
        update.message.reply_text(response)


updater = telegram.ext.Updater(token, use_context=True)
disp = updater.dispatcher

disp.add_handler(telegram.ext.CommandHandler("start", start))
disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, reply))


updater.start_polling()
updater.idle()
