import serial
from telegram import Bot
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Imposta il tuo token Telegram
TELEGRAM_BOT_TOKEN = 'IL_TUO_TOKEN'
# Imposta il tuo chat ID
TELEGRAM_CHAT_ID = 'IL_TUO_CHAT_ID'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Bot avviato!')

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Comando di aiuto!')

def send_help_message():
    # Invia un messaggio a Telegram con scritto "aiuto"
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text='aiuto')

def main() -> None:
    updater = Updater(TELEGRAM_BOT_TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, help_command))

    updater.start_polling()

    ser = serial.Serial('COMx', 9600)  # Sostituisci 'COMx' con il nome della tua porta seriale

    while True:
        arduino_data = ser.readline().decode('utf-8').strip().split(',')[:6]
        if 'aiuto' in arduino_data:
            send_help_message()

    updater.idle()

