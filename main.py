import os
from Crypto.Cipher import AES
import base64
import logging
import emoji
import telegram
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import (
    MessageHandler,
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    Filters,
    CallbackContext,
)


from telegram.utils import helpers

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update, context):
    usr_cmd = update.message.text.split("_")[-1]
    if usr_cmd == "/start":
         update.message.reply_text(
            "<b>Hi {} {} ! \n\nI'm <a href=\"tg://user?id=1535956401\">Storache</a> - A Powerful bot to store all your things safe."
            "\n\nFiles shared to me are kept in a safest place and no one can access it."
            "\n\nHit </b>/help<b> to find out more about how to use me.</b>".format(update.effective_user.first_name, (
                emoji.emojize(":wave:", use_aliases=True))), parse_mode='html',
                reply_to_message_id=update.message.message_id)

    else:
        try:
            file_d = usr_cmd
            key = ''
            iv = ''
            decryption_suite = AES.new(key, AES.MODE_CFB, iv)
            file_id = decryption_suite.decrypt(base64.b64decode(file_d))
            sendFile = context.bot.forward_message(chat_id=update.message.from_user.id, from_chat_id="-1001461051091",
                                                   message_id=int(file_id))
        except:
            context.bot.sendMessage(chat_id=u.message.chat.id, text='File Not Found')

def assist(update, context):
    update.message.reply_text("*Hey! My name is Storache.* "
                              "\n\nI am the safest file store bot, here to help you to keep all your files secure!"
                              "\nI have lots of handy features to help You"
                              "\n\n*Helpful commands:*"
                              "\n\t\t- /start: Starts me! You've probably already used this."
                              "\n\t\t- /help: Sends this message; I'll tell you more about myself!"
                              "\n\t\t- /about : About the bot."
                              "\n\t\t- /donate: Gives you info on how to support me and my creator."
                              "\n\n*Forward or send me any media as a document file to keep safe and I will provide you a permanent URL to access the file anytime at telegram.* ",
                              parse_mode=telegram.ParseMode.MARKDOWN, reply_to_message_id=update.message.message_id)



def storache(update, context):
    if update.message.chat.type == "private":
        editable = update.message.reply_text("Please wait ...")
        try:
            forwarded = context.bot.copy_message(chat_id='',
                                                 from_chat_id=update.message.chat.id,
                                                 message_id=update.message.message_id)

# For a secondary Backup

#            context.bot.copy_message(chat_id='',
#                                     from_chat_id=update.message.chat.id,
#                                     message_id=update.message.message_id)
            file_er_id = forwarded.message_id
            key = ''
            iv = ''
            enc_s = AES.new(key, AES.MODE_CFB, iv)
            cipher_text = enc_s.encrypt(str(file_er_id))
            encoded_cipher_text = base64.b64encode(cipher_text)
            sharelink = f"https://telegram.dog/storacheBot?start=theostrich_{(str(encoded_cipher_text))[2:-1]}"
            context.bot.sendMessage(chat_id='', text=f"*Ache Map:*\n\n*File ID    :* {forwarded.message_id}\n*User ID* :{update.message.chat.id}\n*User Name :* {update.message.chat.username}\n*First Name : *{update.message.chat.first_name}\n*Last Name : *{update.message.chat.last_name}\n*Text :* {update.message.text}",
                                    reply_to_message_id=forwarded.message_id, parse_mode=telegram.ParseMode.MARKDOWN)
# For a secondary Backup

#            context.bot.sendMessage(chat_id='', text=f"*Ache Map:*\n\n*File ID :* {forwarded.message_id}\n*User ID* :{update.message.chat.id}\n*User Name :* {update.message.chat.username}\n*First Name : *{update.message.chat.first_name}\n*Last Name : *{update.message.chat.last_name}\n*Text :* {update.message.text}",
#                                    reply_to_message_id=forwarded.message_id, parse_mode=telegram.ParseMode.MARKDOWN)
            context.bot.editMessageText(f"File stored safely in  a safest place, get it anytime using :\n\n{sharelink}",
                                        chat_id=update.message.chat_id,
                                        message_id=editable.message_id)
        except:
            context.bot.sendMessage(chat_id=update.message.chat.id, text='<b>Something went wrong!</b>\n\n<b>Report this issue:</b>\n\t- @ostrichdiscussion\n\t- @contactOstrichBot',parse_mode='html')
def aboutTheBot(update, context):
    """Log Errors caused by Updates."""

    keyboard = [
        [
            telegram.InlineKeyboardButton((emoji.emojize(":loop:", use_aliases=True)) + "Channel",
                                          url="t.me/theostrich"),
            telegram.InlineKeyboardButton("👥Support Group", url="t.me/ostrichdiscussion"),
        ],
        [telegram.InlineKeyboardButton((emoji.emojize(":bookmark:", use_aliases=True)) + "Add Me In Group",
                                       url="https://t.me/storacheBot?startgroup=new")],
    ]

    reply_markup = telegram.InlineKeyboardMarkup(keyboard)

    update.message.reply_text("<b>Hey! My name is Storache.</b>"
                              "\nI can handle links in different ways."
                              "\n\n<b>About Me :</b>"
                              "\n\n  - <b>Name</b>        : Storache"
                              "\n\n  - <b>Creator</b>      : @theostrich"
                              "\n\n  - <b>Language</b>  : Python 3"
                              "\n\n  - <b>Library</b>       : <a href=\"https://github.com/python-telegram-bot/python-telegram-bot/\">python-telegram-bot</a>"
                              "\n\n  - <b>Source Code</b>  : Currently Unavailable."
                              "\n\nIf you enjoy using me and want to help me survive, do donate with the /donate command - my creator will be very grateful! Doesn't have to be much - every little helps! Thanks for reading :)",
                              parse_mode='html', reply_markup=reply_markup, disable_web_page_preview=True)

def button(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

def donate(update, context):
    keyboard = [
        [
            telegram.InlineKeyboardButton("Contribute",
                                          url="https://github.com/theostrich"),
            telegram.InlineKeyboardButton("Paypal Us",url="https://paypal.me/donateostrich"),
        ],
    ]

    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Thank you for your wish to contribute. I hope you enjoyed using our services. Make a small donation/contribute to let this project alive." , reply_markup=reply_markup)


def main():
    TOKEN = ""

    updater = Updater(TOKEN)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", assist))
    dispatcher.add_handler(CommandHandler("about", aboutTheBot))
    dispatcher.add_handler(CommandHandler("donate", donate))
    dispatcher.add_handler(MessageHandler((Filters.audio | Filters.document | Filters.video), storache))
    updater.start_polling()


if __name__ == "__main__":
    main()
